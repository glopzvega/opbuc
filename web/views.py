from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import login, authenticate
# import locale
from datetime import datetime
import json
import logging
_logger = logging.getLogger(__name__)
# Create your views here.

from .forms import CategoriaModelForm, LugarModelForm, ProductoModelForm, PhotoModelForm, SignupForm

from api import models

def index(request):
	categorias = models.Category.objects.filter(tipo__exact='lugar')
	zonas = models.Zone.objects.all()
	context = {
		"data" : categorias, 
		"zonas" : zonas
	}
	return render(request, "web/index.html", context)

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

	return render(request, 'registration/signup.html', {'form': form})

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

	context = {
		"data" : lugar ,
		"comments" : comments,
		"photos" : photos,
		"productos" : productos,
		"categories" : cats,
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
			zone_id = int(request.GET.get("zone", False))
			zone_ids = models.Zone.objects.filter(id=zone_id)
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
			for lugar in lugares:
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
	
	categorias = models.Category.objects.filter(user=request.user)

	context = {
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
		"data" : cat,
		"form" : form
	}

	return render(request, "web/categoria_editar.html", context)

def ver_lugares(request):
	
	lugares = models.Lugar.objects.all().filter(user=request.user)

	context = {
		"data" : lugares
	}

	return render(request, "web/lugares.html", context)


def lugar_nuevo(request):
	
	if request.method == "POST":
		form = LugarModelForm(request.POST)
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
		form = LugarModelForm()

	context = {
		"form" : form
	}

	return render(request, "web/lugar_nuevo.html", context)

def lugar_editar(request, id):
	lugar = get_object_or_404(models.Lugar, pk=id)

	if request.method == "POST":
		form = LugarModelForm(request.POST, instance=lugar)
		if form.is_valid():
			form.save()
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

	orders = models.Order.objects.filter(usuario=request.user).order_by('-fecha_pedido')

	if orders:
		for oid in orders:
			
			if oid.state == "draft":
				oid.state_txt = "Pendiente"
			else:
				oid.state_txt = "Realizado"

			oid.lines = models.OrderLine.objects.filter(order=oid)

	data = {
		"orders" : orders
	}

	return render(request, "web/orders.html", data)

def detalle_pedido(request, id):

	order = get_object_or_404(models.Order, pk=id)
	
	order.state_txt = "Pendiente"
	if order.state == "done":
		order.state_txt = "Realizado"

	order.lines = models.OrderLine.objects.filter(order=order)

	data = {
		"order" : order
	}

	return render(request, "web/order_detail.html", data)	

def confirmar_compra(request, newOrder):

	if request.method == "GET":
		
		if request.GET.get("conektaTokenId", False):

			import conekta

			conekta.api_key = "key_Gh4y91YYiyTrLcPbuKtyQw"
			conekta.api_version = "2.0.0"

			try:
				token_id = request.GET.get("conektaTokenId", False)
				print(token_id)
				token_id = "tok_test_visa_4242"

				customer = conekta.Customer.create({
					'name': request.user.username,
					'email': request.user.email or "mcgalv@gmail.com",
					'phone': '+52181818181',
					'payment_sources': [{
						'type': 'card',
						'token_id': token_id
					}]
				})
				
				order = conekta.Order.create({
					"line_items": [{
						"name": "Tacos",
						"unit_price": 1000,
						"quantity": 12
					}],
					"shipping_lines": [{
						"amount": 1500,
						"carrier": "FEDEX"
					}], #shipping_lines - physical goods only
					"currency": "MXN",
					"customer_info": {
						"customer_id": customer.id
					},
					"shipping_contact":{
						"address": {
							"street1": "Calle 123, int 2",
							"postal_code": "06100",
							"country": "MX"
						} #shipping_contact - required only for physical goods
					},
					"metadata": {"description": "Compra de creditos: 300(MXN)", "reference": "1334523452345"},
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
				order["shipping_contact"] = vars(order["shipping_contact"])

				print(order)
				order["success"] = True
				return order
				# return JsonResponse(order)

			except conekta.ConektaError as e:												
				print(vars(e))		
				e = vars(e)			
				e["success"] = False
				return e
				# return JsonResponse(e)

	return {"success" : False, "error" : "No se recibieron datos"}
	# return JsonResponse({"success" : False, "error" : "No se recibieron datos"})

def comprar_carrito(request):
	
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
	
	newOrder = models.Order(usuario=request.user, name="/", fecha_pedido=hoy, hora_pedido=ahora, total=total, lugar=lugar)
	newOrder.save()

	if newOrder.id:
		for prod in carrito:
			producto = models.Producto.objects.get(pk=prod["id"])
			if producto:
				line = models.OrderLine(usuario=request.user, order=newOrder, producto=producto, quantity=prod["cantidad_carrito"], subtotal=prod["subtotal"])
				line.save()
		
		res = confirmar_compra(request, newOrder)
			
		if res["success"]:
			newOrder.state = "done"			
			newOrder.payment_info = res
			newOrder.save()

	request.session['carrito'] = []
	request.session['total'] = 0
	request.session['numero'] = 0

	data = {'success': True, 'id' : newOrder.id}	
	return JsonResponse(data)

# @login_required
def ver_carrito(request):

	total = 0
	if not request.session.has_key("carrito"):
		request.session["carrito"] = []

	empty = False
	if not request.session["carrito"]:
		empty = True

	# locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
	
	productos = []
	for el in request.session["carrito"]:
		producto = get_object_or_404(models.Producto, pk=el["id"])
		producto.cantidad_carrito = el["cantidad_carrito"]
		producto.subtotal = el["subtotal"]
		
		# subtotal_txt = locale.currency(producto.subtotal, grouping=True)
		# producto.subtotal_txt = subtotal_txt
		producto.subtotal_txt = "%.2f" % producto.subtotal
		
		# price_txt = locale.currency(producto.price, grouping=True)
		# producto.price_txt = price_txt
		producto.price_txt = "%.2f" % producto.price

		productos.append(producto)

	if "total" in request.session:
		total = request.session["total"]

	# total = locale.currency(total, grouping=True)
	total = "%.2f" % total

	return render(request, "web/carrito.html", {"empty" : empty, "productos" : productos, "total" : total})

# @login_required
def cantidad_carrito(request, id):

	producto = get_object_or_404(models.Producto, pk=id)

	if not request.session.has_key("carrito"):
		request.session["carrito"] = []

	cantidad_carrito = int(request.GET.get("qty", 1))

	carrito = request.session["carrito"]
	total = 0
	subtotal = 0

	for el in carrito:
		if el["id"] == producto.id:
			el["cantidad_carrito"] = cantidad_carrito
			subtotal = float(producto.price) * cantidad_carrito
			el["subtotal"] = subtotal
		total += el["subtotal"]

	request.session["numero"] = len(carrito)
	request.session["total"] = total
	request.session["carrito"] = carrito
	
	# locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
	# total = locale.currency(total, grouping=True)
	# subtotal = locale.currency(subtotal, grouping=True)

	return JsonResponse({"success" : True, "qty" : len(carrito), "subtotal" : subtotal, "total" : total})		

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
	request.session["total"] = total
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

	request.session["numero"] = len(carrito)
	request.session["total"] = total
	request.session["carrito"] = carrito

	# locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
	# total = locale.currency(total, grouping=True)

	return JsonResponse({"success" : True, "qty" : len(carrito), "total" : total})