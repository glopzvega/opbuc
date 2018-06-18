from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
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

	if categoria:
		lugares = models.Lugar.objects.filter(category__exact=id)

	context = {
		"data" : lugares,
		"categoria" : categoria
	}
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
	
	context = {
		"data" : lugar ,
		"photos" : photos
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

def lugar_photo_upload(request, id):
	lugar = get_object_or_404(models.Lugar, pk=id)

	form = PhotoModelForm(request.POST, request.FILES)
	
	if form.is_valid():
		photo = form.save(commit=False)
		photo.name = photo.photo.name
		photo.lugar_id = lugar
		photo.save()
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

	context = {
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