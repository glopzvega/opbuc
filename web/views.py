from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# import locale
from datetime import datetime
import json
from random import choice
import logging
_logger = logging.getLogger(__name__)
# Create your views here.

from .forms import ConfigForm, ConfigAdminForm, CategoriaModelForm, LugarModelForm, ProductoModelForm, PhotoModelForm, SignupForm

from api import models
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

@csrf_exempt
def webhook_payment(request):
	return HttpResponse(status=200)

def verificar_lugar_habilitado(usuario):
	config_ids = models.Config.objects.filter(user=usuario)
	lugar_ids = models.Lugar.objects.filter(user=usuario)
	
	if config_ids and lugar_ids:
		config = config_ids[0]
		lugar = lugar_ids[0]
		if config.conekta_public and config.conekta_private:
			lugar.nuevo = False
		else:
			lugar.nuevo = True
		lugar.save()
	return True

def get_config(request):
	
	usuario = request.user
	config_ids = models.Config.objects.filter(user=usuario)
	if config_ids:
		print(config_ids[0].id)
		config = get_object_or_404(models.Config, pk=config_ids[0].id)
		if request.method == "POST":
			if usuario.is_staff:
				form = ConfigAdminForm(request.POST, request.FILES, instance=config)    				
			else:
				form = ConfigForm(request.POST, request.FILES, instance=config)
			if form.is_valid():
				config = form.save()
				form = ConfigForm(instance=config)

			verificar_lugar_habilitado(config.user)

		else:
			if usuario.is_staff:
				form = ConfigAdminForm(instance=config)	
			else:
				form = ConfigForm(instance=config)	    			
					
	else:
		if request.method == "POST":
			if usuario.is_staff:
				form = ConfigAdminForm(request.POST, request.FILES)
			else:
				form = ConfigForm(request.POST, request.FILES)
			if form.is_valid():
				config = form.save(commit=False)
				config.user = usuario
				config.save()				
				
				verificar_lugar_habilitado(config.user)

				if usuario.is_staff:
					form = ConfigAdminForm(instance=config)
				else:
					form = ConfigForm(instance=config)    				
				
		else:
			if usuario.is_staff:
				form = ConfigAdminForm()	    		
			else:
				form = ConfigForm()	    		
	
	return render(request, "web/config.html", {"form" : form})

def get_mensajes(request):
	return render(request, "web/index.html", {})

def get_usuarios(request):
	usuarios = User.objects.filter(is_staff=False)
	
	for user in usuarios:
		lugares = models.Lugar.objects.filter(user=user)
		if lugares:
			user.lugar = lugares[0]		

	data = {
		"usuarios" : usuarios
	}
	return render(request, "web/usuarios.html", data)

def mail_usuarios(request):
	
	mensaje = request.POST.get("mensaje", "")
	user_ids = request.POST.get("usuarios", [])
	if user_ids:
		user_ids = user_ids.split(",")
	print(user_ids)
	email_list = []
	for uid in user_ids:
		user = User.objects.get(pk=uid)
		if user and user.email and not user.email in email_list:
			email_list.append(user.email)
	
	if email_list:
		print(email_list)
		send_mail(
			'MENSAJE OPBUC',
			mensaje,
			'admin@opbuc.com',
			email_list,
			fail_silently=False,
		)
	
	return JsonResponse({"success" : True})

def bloquear_usuario(request, id):
	usuario = get_object_or_404(User, pk=id)
	if usuario.is_active:
		usuario.is_active = False
		
		lugar_ids = models.Lugar.objects.filter(user=usuario)
		if lugar_ids:
			lugar = lugar_ids[0]
			lugar.nuevo = True
			lugar.save()
	else:
		usuario.is_active = True

		lugar_ids = models.Lugar.objects.filter(user=usuario)
		if lugar_ids:
			lugar = lugar_ids[0]
			lugar.nuevo = False
			lugar.save()

	usuario.save()
	return JsonResponse({"success": True, "id": id, "is_active": usuario.is_active})


def update_usuario(request, id):
	usuario = get_object_or_404(User, pk=id)
	if usuario.is_superuser:
		usuario.is_superuser = False
	else:
		usuario.is_superuser = True

		lugar_ids = models.Lugar.objects.filter(user=usuario)
		if not lugar_ids:
			lugar_name = "Nuevo"
			lugar_nuevo = models.Lugar(name=lugar_name, clear_name=lugar_name, user=usuario)
			lugar_nuevo.save()
	usuario.save()
	return JsonResponse({"success": True, "id": id, "is_superuser": usuario.is_superuser})

def suggest_usuario(request, id):
	lugar = get_object_or_404(models.Lugar, pk=id)
	if lugar.sugerido:
		lugar.sugerido = False
	else:
		lugar.sugerido = True
	lugar.save()
	return JsonResponse({"success": True, "id": id, "sugerido": lugar.sugerido})

def index(request):
	categorias = models.Category.objects.filter(tipo__exact='lugar')
	zonas = models.Zone.objects.all()
	config = models.Config.objects.all()
	context = {
		"data" : categorias, 
		"zonas" : zonas,
		"buscar" : True,
		"config" : config[0]
	}


	return render(request, "web/index.html", context)

# def login_google(request):
# 	if request.method == 'POST' and request.POST.get("username", False):
# 		username = request.POST.get("username")
# 		usuario = User.objects.filter(username=username)
# 		_logger.debug(usuario)
# 		# if usuario:
# 		# 	login(request, usuario[0])
# 		# 	return json.dumps({"success" : True})		
# 		# else:
# 		# 	return json.dumps({"success" : False, "error" : "Usuario no encontrado"})
# 	return json.dumps({"success" : False})

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('index')
	else:
		form = SignupForm()

	config = models.Config.objects.all()

	return render(request, 'registration/signup.html', {
		'form': form,
		'config' : config[0]
		})

def signup_host(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			new_user.is_superuser = True
			new_user.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('index')
	else:
		form = SignupForm()
	
	config = models.Config.objects.all()

	return render(request, 'registration/signup.html', {
		'form': form,
		'config' : config[0]
	})

def zonas(request):
	zonas = models.Zone.objects.all()
	context = {
		"data" : zonas 
	}
	return render(request, "web/index.html", context)

def categorias_lugar(request):
	categorias = models.Category.objects.filter(tipo__exact='lugar')
	context = {
		"data" : categorias 
	}
	return render(request, "web/index.html", context)

def categorias_producto(request):
	categorias = models.Category.objects.filter(tipo__exact='producto')
	context = {
		"data" : categorias 
	}
	return render(request, "web/index.html", context)

def lugares_zona(request, id):
	zona = get_object_or_404(models.Zone, pk=id)	
	lugares = []

	if zona:
		lugares = models.Lugar.objects.filter(zone__exact=id)

	context = {
		"data" : lugares,
		"zona" : zona
	}
	return render(request, "web/zona_detail.html", context)

def lugares_categoria(request, id):

	categoria = get_object_or_404(models.Category, pk=id)	
	lugares = []

	RequestType = request.GET.get("type", False)
	
	if categoria:
		lugares = models.Lugar.objects.filter(category__exact=id)

	zones = models.Zone.objects.all()

	zone = request.GET.get("zone", False)	

	if zone:
		lugares = lugares.filter(zone_id=zone)
		zone = models.Zone.objects.get(id=zone)		

	context = {
		"categoria" : categoria,
		"data" : lugares,
		"zones" : zones,
		"zone" : zone
	}

	if RequestType and RequestType == "json":
		
		items = []
		for lugar in lugares:
			item = {
				"id" : lugar.id,
				"name" : lugar.name,
				"zone" : {
					"id" : lugar.zone.id,
					"name" : lugar.zone.name,
				},
				"address" : lugar.address,
				"phone" : lugar.phone,
				"email" : lugar.email,				
				"photo" : lugar.photo.url
			}
			# if lugar.photo and lugar.photo.url:
			# 	item["photo"] = lugar.photo.url

			items.append(item)		

		data = {
			"success" :  True,
			"zone" : False,
			"data" : items,			
		}

		if zone: 
			data["zone"] = {
					"id" : zone.id,
					"name" : zone.name
				} 

		return JsonResponse(data)
	
	else:
		return render(request, "web/categoria_detail.html", context)
		


def lugares_categoria_zona(request, id, zone_id):
	categoria = get_object_or_404(models.Category, pk=id)	
	lugares = []

	if categoria:
		zona = get_object_or_404(models.Zone, pk=zone_id)

		if zona:
			lugares = models.Lugar.objects.filter(category__exact=id).filter(zone__exact=zone_id)

	context = {
		"data" : lugares
	}

	return render(request, "web/categoria_detail.html", context)

def lugar(request, id):
	lugar = get_object_or_404(models.Lugar, pk=id)	
	photos = models.Photo.objects.filter(lugar_id__exact=id)
	productos = models.Producto.objects.filter(lugar=lugar)	
	comments = models.Comment.objects.filter(lugar=lugar)
	zonas = models.Zone.objects.all()
	
	cats = []
	for prod in productos:
		cat = prod.category
		existe = False
		for c in cats:
			if c.id == cat.id:
				existe = True
				break
		if not existe:
			cats.append(cat)

	for cat in cats:
		cat.prods = productos.filter(category=cat)

	calif = 0
	prom = 0
	for comm in comments:
		calif += comm.puntuacion
	if calif > 0:
		prom = calif / len(comments)

	config = False
	config_ids = models.Config.objects.filter(user=lugar.user)
	if config_ids:
		config = config_ids[0]

	# lugares = models.Lugar.objects.filter(~Q(id=id))[:3]
	lugares = models.Lugar.objects.filter(nuevo=False).filter(sugerido=True)[:3]
	context = {
		"data" : lugar ,
		"comments" : comments,
		"calificacion" : len(comments),
		"promedio" : round(prom),
		"photos" : photos,
		"productos" : productos,
		"categories" : cats,
		"lugares" : lugares,
		"config" : config
		# "config" : config
		# "zonas" : zonas
	}
	return render(request, "web/lugar_detail.html", context)

def buscarlugar(request):
	data = []
	if request.method == "GET":
		lugares = models.Lugar.objects.all()
		
		if request.GET.get("busqueda", False):			
			busqueda = request.GET.get("busqueda", False)			
			lugares = lugares.filter(clear_name__icontains=busqueda)

		if request.GET.get("zone", False):
			print("#### ZONE ####")
			zone_id = int(request.GET.get("zone", False))
			print(zone_id)			
			zone_ids = models.Zone.objects.filter(id=zone_id)
			print(zone_ids)
			if zone_ids:
				zone = zone_ids[0]
				lugares = lugares.filter(zone=zone)

		if request.GET.get("category", False):			
			category_id = int(request.GET.get("category", False))
			category_ids = models.Category.objects.filter(id=category_id)
			if category_ids:
				category = category_ids[0]
				lugares = lugares.filter(category=category)

		if lugares:
			data = []
			for lugar in lugares.filter(nuevo=False):
				lugar_data = {
						"id" : lugar.id,
						"name" : lugar.name,
						"video" : lugar.video,
						"photo" : lugar.photo and lugar.photo.url or "",
						"description" : lugar.description,
						"zone_id" : lugar.zone_id,
						"category_id" : lugar.category_id,
						"phone" : lugar.phone,
						"address" : lugar.address,
						"email" : lugar.email,
					}
				if lugar.zone_id:
					zone = models.Zone.objects.get(pk=lugar.zone_id)
					if zone:
						lugar_data["zone_id"] = (zone.id, zone.name)

				data.append(lugar_data)
	
	return JsonResponse({"data" : data})

def producto(request, id):
	producto = get_object_or_404(models.Producto, pk=id)	
	photos = models.Photo.objects.filter(producto_id__exact=id)
	
	context = {
		"data" : producto,
		"photos" : photos
	}
	return render(request, "web/producto_detail.html", context)

def ver_categorias(request):
	
	categorias = models.Category.objects.filter(user=request.user).filter(tipo="producto").filter(status="active")

	context = {
		"tipo" : "producto",
		"data" : categorias
	}

	return render(request, "web/categorias.html", context)

def ver_categorias_lugares(request):
		
	categorias = models.Category.objects.filter(tipo="lugar").filter(status="active")

	context = {
		"tipo" : "lugar",
		"data" : categorias
	}

	return render(request, "web/categorias.html", context)


def categoria_nuevo(request):
	
	if request.method == "POST":
		form = CategoriaModelForm(request.POST, request.FILES)
		if form.is_valid():
			cat = form.save(commit=False)
			cat.tipo = 'producto'
			cat.user = request.user
			cat.save()
			return redirect("ver_categorias")
	else:
		form = CategoriaModelForm()

	context = {
		"tipo" : "producto", 
		"form" : form
	}

	return render(request, "web/categoria_nuevo.html", context)

def categoria_lugar_nuevo(request):
		
	if request.method == "POST":
		form = CategoriaModelForm(request.POST, request.FILES)
		if form.is_valid():
			cat = form.save(commit=False)
			cat.tipo = 'lugar'
			cat.user = request.user
			cat.save()
			return redirect("ver_categorias_lugares")
	else:
		form = CategoriaModelForm()

	context = {
		"tipo" : "lugar",
		"form" : form
	}

	return render(request, "web/categoria_nuevo.html", context)

def categoria_editar(request, id):
	cat = get_object_or_404(models.Category, pk=id)

	if request.method == "POST":
		form = CategoriaModelForm(request.POST, request.FILES, instance=cat)
		if form.is_valid():
			form.save()
			return redirect("ver_categorias")
	else:
		form = CategoriaModelForm(instance=cat)

	context = {
		"tipo" : "producto",
		"data" : cat,
		"form" : form
	}

	return render(request, "web/categoria_editar.html", context)

def categoria_lugar_editar(request, id):
	cat = get_object_or_404(models.Category, pk=id)

	if request.method == "POST":
		form = CategoriaModelForm(request.POST, request.FILES, instance=cat)
		if form.is_valid():
			form.save()
			return redirect("ver_categorias_lugares")
	else:
		form = CategoriaModelForm(instance=cat)

	context = {
		"tipo" : "lugar",
		"data" : cat,
		"form" : form
	}

	return render(request, "web/categoria_editar.html", context)

def categoria_bloquear(request, id):
	
	cat = get_object_or_404(models.Category, pk=id)	
	
	if cat.tipo == "producto":
		product_ids = models.Producto.objects.filter(category=cat)
		if not product_ids:
			cat.status = "cancel"
			cat.save()
			return JsonResponse({"success" : True})
		mensaje = "La categoria no puede eliminarse, hay productos relacionados con la categoria"
	else:
		lugar_ids = models.Lugar.objects.filter(category=cat)
		if not lugar_ids:
			cat.status = "cancel"
			cat.save()
			return JsonResponse({"success" : True})
		mensaje = "La categoria no puede eliminarse, hay lugares relacionados con la categoria"
		
	return JsonResponse({"success" : False, "mensaje" : mensaje})

def ver_lugares(request):
	
	lugares = models.Lugar.objects.all().filter(user=request.user)

	context = {
		"data" : lugares
	}

	return render(request, "web/lugares.html", context)


def lugar_nuevo(request):
	
	if request.method == "POST":
		form = LugarModelForm(request.POST, request.FILES)

		if form.is_valid():
			lugar = form.save(commit=False)
			clear_name = lugar.name.lower()
			clear_name = clear_name.replace("á", "a")
			clear_name = clear_name.replace("é", "e")
			clear_name = clear_name.replace("í", "i")
			clear_name = clear_name.replace("ó", "o")
			clear_name = clear_name.replace("ú", "u")
			lugar.clear_name = clear_name.replace("ñ", "n")
			lugar.user = request.user
			lugar.save()
			return redirect("ver_lugares")
	
	else:	
		
		lugares = models.Lugar.objects.filter(user=request.user)		
		if lugares and not request.user.is_staff:
			return redirect("ver_lugares")

		form = LugarModelForm()

	context = {
		"form" : form
	}

	return render(request, "web/lugar_nuevo.html", context)

def lugar_editar(request, id):
	lugar = get_object_or_404(models.Lugar, pk=id)

	if request.method == "POST":
		form = LugarModelForm(request.POST, request.FILES, instance=lugar)
		if form.is_valid():
			lugar = form.save(commit=False)
			clear_name = lugar.name.lower()
			clear_name = clear_name.replace("á", "a")
			clear_name = clear_name.replace("é", "e")
			clear_name = clear_name.replace("í", "i")
			clear_name = clear_name.replace("ó", "o")
			clear_name = clear_name.replace("ú", "u")
			lugar.clear_name = clear_name.replace("ñ", "n")			
			lugar.save()
			return redirect("ver_lugares")
	else:
		form = LugarModelForm(instance=lugar)

	fotos = models.Photo.objects.filter(lugar_id__exact=lugar)

	context = {
		"fotos" : fotos,
		"data" : lugar,
		"form" : form
	}

	return render(request, "web/lugar_editar.html", context)

def lugar_comment_upload(request, id):

	lugar = get_object_or_404(models.Lugar, pk=id)

	comentario = request.GET.get("comentario", False)
	puntuacion = request.GET.get("puntuacion", False)
	if comentario and puntuacion:
		newComment = models.Comment(usuario=request.user, comentario=comentario, puntuacion=puntuacion, lugar=lugar)
		newComment.save()

		if newComment.id:
			return JsonResponse({"success" : True, "id" : newComment.id})

	return JsonResponse({"success" : False})

def producto_photo_upload(request, id):
	producto = get_object_or_404(models.Producto, pk=id)

	form = PhotoModelForm(request.POST, request.FILES)
	
	if form.is_valid():
		photo = form.save(commit=False)
		photo.name = photo.photo.name
		photo.producto_id = producto
		photo.save()

		if not producto.photo:
			producto.photo = photo.photo
			producto.save()

		data = {'success': True, 'name': photo.photo.name, 'url': photo.photo.url}
	
	else:
		data = {'success': False}
	
	return JsonResponse(data)

def lugar_photo_upload(request, id):
	lugar = get_object_or_404(models.Lugar, pk=id)

	form = PhotoModelForm(request.POST, request.FILES)
	
	if form.is_valid():
		photo = form.save(commit=False)
		photo.name = photo.photo.name
		photo.lugar_id = lugar
		photo.save()

		if not lugar.photo:
			lugar.photo = photo.photo
			lugar.save()

		data = {'success': True, 'name': photo.photo.name, 'url': photo.photo.url}
	
	else:
		data = {'success': False}
	
	return JsonResponse(data)

def ver_productos(request):
	
	lugares = models.Lugar.objects.filter(user=request.user)
	productos = models.Producto.objects.all().filter(lugar__in=lugares)

	context = {
		"data" : productos
	}

	return render(request, "web/productos.html", context)


def producto_nuevo(request):
	
	if request.method == "POST":
		form = ProductoModelForm(request.user, request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect("ver_productos")
	else:
		form = ProductoModelForm(request.user)

	context = {
		"form" : form
	}

	return render(request, "web/producto_nuevo.html", context)

def producto_editar(request, id):
	producto = get_object_or_404(models.Producto, pk=id)

	if request.method == "POST":
		form = ProductoModelForm(request.user, request.POST, request.FILES, instance=producto)
		if form.is_valid():
			form.save()
			return redirect("ver_productos")
	else:
		form = ProductoModelForm(request.user, instance=producto)

	fotos = models.Photo.objects.filter(producto_id=producto)

	context = {
		"fotos" : fotos,
		"data" : producto,
		"form" : form
	}

	return render(request, "web/producto_editar.html", context)

def producto_fotos(request, id):
	producto = get_object_or_404(models.Producto, pk=id)
	fotos = models.Photo.objects.filter(producto_id__exact=producto)	
	context = {
		"data" : fotos
	}

	return render(request, "web/producto_fotos.html", context)

def eliminar_foto(request, id):
	producto = get_object_or_404(models.Photo, pk=id)
	res = producto.delete()
	
	if res:
		data = {'success': True}	
	else:
		data = {'success': False}	

	return JsonResponse(data)

def main_foto(request, id):
	
	photo = get_object_or_404(models.Photo, pk=id)	

	tipo = request.GET.get("tipo")
	
	if tipo == "lugar":
		lugar = get_object_or_404(models.Lugar, pk=photo.lugar_id.id)
		lugar.photo = photo.photo
		lugar.save()

	elif tipo == "producto":
		producto = get_object_or_404(models.Producto, pk=photo.producto_id.id)
		producto.photo = photo.photo
		producto.save()	

	data = {'success': True, 'url': photo.photo.url}	
	
	return JsonResponse(data)

def ver_pedidos(request):

	orders = []

	if request.user.is_staff:
		orders = models.Order.objects.all().order_by('-fecha_pedido')
	elif request.user.is_superuser:
		lugares = models.Lugar.objects.filter(user=request.user)
		if lugares:
			lugar = lugares[0]
			orders = models.Order.objects.filter(lugar=lugar).filter(~Q(status_entrega="done")).filter(~Q(status_entrega="cancel")).order_by('-fecha_pedido')

	else:
		orders = models.Order.objects.filter(usuario=request.user).filter(~Q(status_entrega="done")).filter(~Q(status_entrega="cancel")).order_by('-fecha_pedido')	

	if orders:
		for oid in orders:
			
			if oid.state == "draft":
				oid.state_txt = "Pendiente"
			else:
				oid.state_txt = "Realizado"

			if oid.status_entrega == 'draft':
				oid.status_entrega_txt = 'Pendiente'
			elif oid.status_entrega == 'open':
				oid.status_entrega_txt = 'En proceso'
			elif oid.status_entrega == 'done':
				oid.status_entrega_txt = 'Entregada'
			else:
				oid.status_entrega_txt = 'Cancelada'

			oid.lines = models.OrderLine.objects.filter(order=oid)

	data = {
		"user" : request.user,
		"orders" : orders
	}

	return render(request, "web/orders.html", data)

def detalle_pedido(request, id):

	order = get_object_or_404(models.Order, pk=id)
	
	order.state_txt = "Pendiente"
	if order.state == "done":
		order.state_txt = "Realizado"

	if order.status_entrega == 'draft':
		order.status_entrega_txt = 'Pendiente'
	elif order.status_entrega == 'open':
		order.status_entrega_txt = 'En Proceso'
	elif order.status_entrega == 'done':
		order.status_entrega_txt = 'Entregada'
	else:
		order.status_entrega_txt = 'Cancelada'

	order.subtotal = float(order.total) + order.cupon

	order.lines = models.OrderLine.objects.filter(order=order)

	data = {
		"user" : request.user,
		"order" : order
	}

	return render(request, "web/order_detail.html", data)

def validar_pedido(request, id):
		
	order = get_object_or_404(models.Order, pk=id)
	
	order.status_entrega = "open"
	order.save()

	data = {
		"order" : order
	}

	return redirect("detalle_pedido", order.id)

def entregar_pedido(request, id):
	
	order = get_object_or_404(models.Order, pk=id)
	
	order.status_entrega = "done"
	order.save()

	data = {
		"order" : order
	}

	return redirect("detalle_pedido", order.id)

def cancelar_pedido(request, id):
	
	order = get_object_or_404(models.Order, pk=id)
	
	order.status_entrega = "cancel"
	order.save()
	
	data = {
		"order" : order
	}

	return redirect("detalle_pedido", order.id)	

def _get_config_usuario(user):
	config_ids = models.Config.objects.filter(user=user)
	if config_ids:
		return config_ids[0]
	return False

def pago_conekta(request, token_id, monto, description, usuario):
	
	try:

		import conekta

		config = _get_config_usuario(usuario)
		if not config:
			return {"success" : False, "error" : "No se encontro configuracion de pago para esta cuenta"}

		conekta.api_key = config.conekta_private
		# conekta.api_key = "key_Gh4y91YYiyTrLcPbuKtyQw"
		conekta.api_version = "2.0.0"

		customer = conekta.Customer.create({
			'name': "%s %s" % (request.user.first_name, request.user.last_name,),
			'email': request.user.email,
			# 'phone': '+52181818181',
			'payment_sources': [{
				'type': 'card',
				'token_id': token_id
			}]
		})
		
		# carrito = request.session["carrito"]
		# line_items = []
		# for prod in carrito:
		# 	producto = models.Producto.objects.get(pk=prod["id"])
		# 	if producto:
		# 		line_items.append({
		# 			"name" : producto.name,
		# 			"unit_price" : producto.price,
		# 			"quantity" : 1
		# 		})

		order = conekta.Order.create({
			"line_items": [{
				"name": "Compra Opbuc",
				"unit_price": monto,
				"quantity": 1
			}],
			# "shipping_lines": [{
			# 	"amount": 1500,
			# 	"carrier": "FEDEX"
			# }], #shipping_lines - physical goods only
			"currency": "MXN",
			"customer_info": {
				"customer_id": customer.id
			},
			# "shipping_contact":{
			# 	"address": {
			# 		"street1": "Calle 123, int 2",
			# 		"postal_code": "06100",
			# 		"country": "MX"
			# 	} #shipping_contact - required only for physical goods
			# },
			"metadata": {"description": "", "reference": description},
			"charges":[{
				"payment_method": {
					"type": "default"
				}  #payment_method - use the customer's default - a card
			 #to charge a card, different from the default,
			 #you can indicate the card's source_id as shown in the Retry Card Section
			}]
		})

		customerJson = vars(customer)
		del customerJson["payment_sources"]
		# print(customerJson)
		
		# print(vars(order))
		order = vars(order)
		line_items = order["line_items"]
		shipping_lines = order["shipping_lines"]
		charges = order["charges"]
						
		line_ids = []
		for line in line_items:
			line = vars(line)
			del line["parent"]
			line_ids.append(line)

		# print(line_ids)

		shipping_ids = []
		for line in shipping_lines:
			line = vars(line)
			del line["parent"]
			shipping_ids.append(line)

		# print(shipping_ids)

		charges_ids = []
		for charge in charges:
			charge = vars(charge)
			# del charge["parent"]
			charge["payment_method"] = vars(charge["payment_method"])
			charges_ids.append(charge)

		# print(charges_ids)

		order["customer_info"] = customerJson
		order["line_items"] = line_ids
		order["shipping_lines"] = shipping_ids
		order["charges"] = charges_ids
		# order["shipping_contact"] = vars(order["shipping_contact"])

		return order

	except conekta.ConektaError as e:												
		print(vars(e))		
		e = vars(e)			
		e["success"] = False
		return e

def confirmar_compra(request, lugar, ref, total):

	if request.method == "GET":
		
		if request.GET.get("conektaTokenId", False):
			
			token_id = request.GET.get("conektaTokenId", False)
			# token_id_admin = request.GET.get("conektaTokenIdAdmin", False)

			print("### TOKEN ID ###")
			print(token_id)
		
			# monto_opbuc = total * 100
			monto_opbuc = 300			
								
			usuario = get_object_or_404(User, pk=1)
			order = pago_conekta(request, token_id, monto_opbuc, ref, lugar.user)
			if "error_json" in order:
				order["success"] = False
				return order

			order["success"] = True
			return order

	return {"success" : False, "error" : "No se recibieron datos"}

def registrar_compra(request):
	
	if not request.session.has_key("carrito"):
		request.session["carrito"] = []

	carrito = request.session["carrito"]

	if not carrito:
		data = {'success': False, 'id' : 0, 'error' : 'El carrito está vacío'}	
		return JsonResponse(data)

	lugar_id = request.session["lugar"]
	lugar = get_object_or_404(models.Lugar, pk=lugar_id)

	hoy = datetime.now().strftime("%Y-%m-%d")
	ahora = datetime.now().strftime("%H:%M:%S")
	
	total = 0
	if "total" in request.session:
		total = request.session["total"]

	cupon = 0
	if "cupon" in request.session:
		cupon = request.session["cupon"]

	invitados = 1
	if "invitados" in request.session:
		invitados = request.session["invitados"]

	ref = ""
	ref = ref.join([choice("0123456789") for i in range(10)])
	
	res = confirmar_compra(request, lugar, ref, total)
	
	print("############")
	print(res)
	
	if res["success"]:

		newOrder = models.Order(usuario=request.user, name=ref, fecha_pedido=hoy, hora_pedido=ahora, total=total, lugar=lugar, cupon=cupon, invitados=invitados)
		newOrder.save()

		if newOrder.id:
			for prod in carrito:
				producto = models.Producto.objects.get(pk=prod["id"])
				if producto:
					line = models.OrderLine(usuario=request.user, order=newOrder, producto=producto, quantity=prod["cantidad_carrito"], subtotal=prod["subtotal"])
					line.save()
		
			newOrder.payment_id = res["id"]
			newOrder.state = "done"			
			newOrder.payment_info = res
			newOrder.save()

			request.session['carrito'] = []
			request.session['total'] = 0
			request.session['numero'] = 0			
			
			res = {'success': True, 'id' : newOrder.id}
			return JsonResponse(res)
			
		else:
			res = {'success': False, 'message' : "No se pudo crear la orden"}

	return JsonResponse(res)

@login_required
def ver_carrito(request):

	total = 0
	subtotal = 0
	invitados = 0
	cupon = 0
	if not request.session.has_key("carrito"):
		request.session["carrito"] = []

	empty = False
	if not request.session["carrito"]:
		empty = True

	# locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
	
	productos = []
	lugar = False
	for el in request.session["carrito"]:
		producto = get_object_or_404(models.Producto, pk=el["id"])
		producto.cantidad_carrito = el["cantidad_carrito"]
		producto.subtotal = el["subtotal"]

		lugar = producto.lugar
		
		# subtotal_txt = locale.currency(producto.subtotal, grouping=True)
		# producto.subtotal_txt = subtotal_txt
		producto.subtotal_txt = "%.2f" % producto.subtotal
		
		# price_txt = locale.currency(producto.price, grouping=True)
		# producto.price_txt = price_txt
		producto.price_txt = "%.2f" % producto.price

		productos.append(producto)

	config = False
	if lugar:    	
		config_ids = models.Config.objects.filter(user=lugar.user)
		if config_ids:
			config = config_ids[0]

	# configAdmin = False
	# usuario = get_object_or_404(User, pk=1)
	# config_ids = models.Config.objects.filter(user=usuario)
	# if config_ids:
	# 	configAdmin = config_ids[0]

	if "invitados" in request.session:
		invitados = request.session["invitados"]

	if "subtotal" in request.session:		
		subtotal = request.session["subtotal"]

	if "total" in request.session:		
		total = request.session["total"]

	if "cupon" in request.session:
		cupon = request.session["cupon"]
		total = subtotal - cupon

	# total = locale.currency(total, grouping=True)
	total = "%.2f" % total

	return render(request, "web/carrito.html", {"empty" : empty, "productos" : productos, "total" : total, "subtotal" : subtotal, "invitados" : invitados, "cupon" : cupon, "config" : config})
	# return render(request, "web/carrito.html", {"empty" : empty, "productos" : productos, "total" : total, "subtotal" : subtotal, "invitados" : invitados, "cupon" : cupon, "config" : config, "configAdmin" : configAdmin})

# @login_required
def cantidad_carrito(request, id):

	producto = get_object_or_404(models.Producto, pk=id)

	if not request.session.has_key("carrito"):
		request.session["carrito"] = []

	cantidad_carrito = int(request.GET.get("qty", 1))
	carrito = request.session["carrito"]
	
	total = 0
	subtotal = 0
	find = False
	for el in carrito:
		if el["id"] == producto.id:
			if cantidad_carrito == 0:
				carrito.remove(el)
				break
			find = True	
			el["cantidad_carrito"] = cantidad_carrito
			subtotal = float(producto.price) * cantidad_carrito
			el["subtotal"] = subtotal
		total += el["subtotal"]

	if not find and cantidad_carrito > 0:		

		if lugar != producto.lugar.id:
			request.session["lugar"] = producto.lugar.id
			# carrito = []

		prod = {
			"id" : producto.id,
			"nombre" : producto.name,
			"descripcion" : producto.description,
			# "imagen" : producto.imagen,
			"categoria_id" : producto.category.id,
			"categoria" : producto.category.name,
			"precio" : float(producto.price),
			# "cantidad" : cantidad,
			"cantidad_carrito" : cantidad_carrito,
			"subtotal" : float(producto.price) * cantidad_carrito,			
			"lugar" : producto.lugar.name,
			"lugar_id" : producto.lugar.id,
		}

		carrito.append(prod)

	cupon = 0
	subtotal = total
	if "cupon" in request.session and request.session["cupon"] > 0:
		cupon = request.session["cupon"]
		total = subtotal - cupon    	

	request.session["numero"] = len(carrito)
	request.session["subtotal"] = subtotal
	request.session["total"] = total
	request.session["carrito"] = carrito
	
	# locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
	# total = locale.currency(total, grouping=True)
	# subtotal = locale.currency(subtotal, grouping=True)

	return JsonResponse({"success" : True, "qty" : cantidad_carrito, "subtotal" : subtotal, "total" : total, "cupon" : cupon})		

def compra_reservar(request, id):
	
	# request.session["carrito"] = []

	lugar = get_object_or_404(models.Lugar, pk=id)
	cupon = lugar.promociones
	
	try:
		invitados = int(request.GET.get("invitados", 1))
	except:
		invitados = 1
		pass
	
	request.session["invitados"] = invitados
	request.session["cupon"] = cupon

	subtotal = 0
	if "subtotal" in request.session:
		subtotal = request.session["subtotal"]
	
	request.session["total"] = subtotal - cupon

	return JsonResponse({"success" : True, "invitados" : invitados, "cupon" : cupon})		

# @login_required
def agregar_carrito(request, id):

	producto = get_object_or_404(models.Producto, pk=id)

	if not request.session.has_key("carrito"):
		request.session["carrito"] = []

	if not request.session.has_key("lugar"):
		request.session["lugar"] = False
		
	carrito = request.session["carrito"]
	lugar = request.session["lugar"]

	find = False		
	for el in carrito:
		if el["id"] == producto.id:
			find = True			
			el["cantidad_carrito"] += 1 
			el["subtotal"] = float(producto.price) * el["cantidad_carrito"]			
			break

	if not find:		

		if lugar != producto.lugar.id:
			request.session["lugar"] = producto.lugar.id
			carrito = []

		prod = {
			"id" : producto.id,
			"nombre" : producto.name,
			"descripcion" : producto.description,
			# "imagen" : producto.imagen,
			"categoria_id" : producto.category.id,
			"categoria" : producto.category.name,
			"precio" : float(producto.price),
			# "cantidad" : cantidad,
			"cantidad_carrito" : 1,
			"subtotal" : float(producto.price),			
			"lugar" : producto.lugar.name,
			"lugar_id" : producto.lugar.id,
		}

		carrito.append(prod)

	total = 0
	for el in carrito:
		total += el["subtotal"]

	request.session["numero"] = len(carrito)
	request.session["subtotal"] = total
	# request.session["total"] = total
	request.session["carrito"] = carrito

	return JsonResponse({"success" : True, "qty" : len(carrito)})

# @login_required
def quitar_carrito(request, id):

	producto = get_object_or_404(models.Producto, pk=id)

	if not request.session.has_key("carrito"):
		request.session["carrito"] = []
		
	carrito = request.session["carrito"]	
	
	for el in carrito:
		if el["id"] == producto.id:
			carrito.remove(el)			
			break

	total = 0
	for el in carrito:
		total += el["subtotal"]
	
	invitados = 0
	if invitados in request.session:
		invitados = request.session["invitados"]
	
	subtotal = total
	if subtotal == 0:
		cupon = 0
		total = 0
		invitados = 0
	elif "cupon" in request.session:
		cupon = request.session["cupon"]
		total = subtotal - cupon

	request.session["numero"] = len(carrito)
	request.session["invitados"] = invitados
	request.session["subtotal"] = subtotal
	request.session["total"] = total
	request.session["cupon"] = cupon
	request.session["carrito"] = carrito

	# locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
	# total = locale.currency(total, grouping=True)

	return JsonResponse({"success" : True, "qty" : len(carrito), "total" : total, "subtotal" : subtotal, "cupon" : cupon, "invitados" : invitados})