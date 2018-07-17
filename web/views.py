from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core import serializers
import locale
# Create your views here.

from .forms import CategoriaModelForm, LugarModelForm, ProductoModelForm, PhotoModelForm

from api import models

def index(request):
	categorias = models.Category.objects.filter(tipo__exact='lugar')
	zonas = models.Zone.objects.all()
	context = {
		"data" : categorias, 
		"zonas" : zonas
	}
	return render(request, "web/index.html", context)

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
	context = {
		"data" : lugar ,
		"comments" : comments,
		"photos" : photos,
		"productos" : productos
	}
	return render(request, "web/lugar_detail.html", context)


def producto(request, id):
	producto = get_object_or_404(models.Producto, pk=id)	
	photos = models.Photo.objects.filter(producto_id__exact=id)
	
	context = {
		"data" : producto,
		"photos" : photos
	}
	return render(request, "web/producto_detail.html", context)

def ver_categorias(request):
	
	categorias = models.Category.objects.all()

	context = {
		"data" : categorias
	}

	return render(request, "web/categorias.html", context)


def categoria_nuevo(request):
	
	if request.method == "POST":
		form = CategoriaModelForm(request.POST)
		if form.is_valid():
			form.save()
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
		form = CategoriaModelForm(request.POST, instance=cat)
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
	
	lugares = models.Lugar.objects.all()

	context = {
		"data" : lugares
	}

	return render(request, "web/lugares.html", context)


def lugar_nuevo(request):
	
	if request.method == "POST":
		form = LugarModelForm(request.POST)
		if form.is_valid():
			form.save()
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
	
	productos = models.Producto.objects.all()

	context = {
		"data" : productos
	}

	return render(request, "web/productos.html", context)


def producto_nuevo(request):
	
	if request.method == "POST":
		form = ProductoModelForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect("ver_productos")
	else:
		form = ProductoModelForm()

	context = {
		"form" : form
	}

	return render(request, "web/producto_nuevo.html", context)

def producto_editar(request, id):
	producto = get_object_or_404(models.Producto, pk=id)

	if request.method == "POST":
		form = ProductoModelForm(request.POST, request.FILES, instance=producto)
		if form.is_valid():
			form.save()
			return redirect("ver_productos")
	else:
		form = ProductoModelForm(instance=producto)

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

# @login_required
def ver_carrito(request):

	total = 0
	if not request.session.has_key("carrito"):
		request.session["carrito"] = []

	empty = False
	if not request.session["carrito"]:
		empty = True

	locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
	
	productos = []
	for el in request.session["carrito"]:
		producto = get_object_or_404(models.Producto, pk=el["id"])
		producto.cantidad_carrito = el["cantidad_carrito"]
		producto.subtotal = el["subtotal"]
		
		subtotal_txt = locale.currency(producto.subtotal, grouping=True)
		producto.subtotal_txt = subtotal_txt
		
		price_txt = locale.currency(producto.price, grouping=True)
		producto.price_txt = price_txt

		productos.append(producto)

	if "total" in request.session:
		total = request.session["total"]

	total = locale.currency(total, grouping=True)

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
	
	locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
	total = locale.currency(total, grouping=True)
	subtotal = locale.currency(subtotal, grouping=True)

	return JsonResponse({"success" : True, "qty" : len(carrito), "subtotal" : subtotal, "total" : total})		

# @login_required
def agregar_carrito(request, id):

	producto = get_object_or_404(models.Producto, pk=id)

	if not request.session.has_key("carrito"):
		request.session["carrito"] = []
		
	carrito = request.session["carrito"]
		
	find = False		
	for el in carrito:
		if el["id"] == producto.id:
			find = True			
			el["cantidad_carrito"] += 1 
			el["subtotal"] = float(producto.price) * el["cantidad_carrito"]			
			break

	if not find:

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

	locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')
	total = locale.currency(total, grouping=True)

	return JsonResponse({"success" : True, "qty" : len(carrito), "total" : total})