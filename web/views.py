from django.shortcuts import render

# Create your views here.

from api import models

def index(request):
	zonas = models.Zone.objects.all()
	context = {
		"data" : zonas 
	}
	return render(request, "web/index.html", context)