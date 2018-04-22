from django.shortcuts import render, get_object_or_404

# Create your views here.

from api import models

def index(request):
	categorias = models.Category.objects.all()
	context = {
		"data" : categorias 
	}
	return render(request, "web/index.html", context)

def zonas(request):
	zonas = models.Zone.objects.all()
	context = {
		"data" : zonas 
	}
	return render(request, "web/index.html", context)

def zona(request, id):
	zona = get_object_or_404(request, pk=id)
	zonas = models.Zone.objects.all()
	context = {
		"data" : zonas 
	}
	return render(request, "web/index.html", context)