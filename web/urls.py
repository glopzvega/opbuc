from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('zona/', views.zonas, name="zonas"),

    path('zona/<int:id>', views.lugares_zona, name="lugares_zona"),
    path('categoria/<int:id>', views.lugares_categoria, name="lugares_categoria"),
    path('categoria/<int:id>/zona/<int:zone_id>', views.lugares_categoria_zona, name="lugares_categoria_zona"),
    
    path('lugar/<int:id>', views.lugar, name="lugar"),
    path('producto/<int:id>', views.producto, name="producto"),

] 
