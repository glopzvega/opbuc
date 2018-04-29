from django.shortcuts import render, get_object_or_404

# Create your views here.

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
		lugares = model.Lugar.objects.filter(zone__exact=id)

	context = {
		"data" : lugares
	}
	return render(request, "web/zona_detail.html", context)

def lugares_categoria(request, id):
	categoria = get_object_or_404(models.Category, pk=id)	
	lugares = []

	if categoria:
		lugares = models.Lugar.objects.filter(category__exact=id)

	context = {
		"data" : lugares
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