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

    # ADMIN URL
    path('categorias/', views.ver_categorias, name="ver_categorias"),
    path('categoria/nuevo', views.categoria_nuevo, name="categoria_nuevo"),
    path('categoria/editar/<int:id>', views.categoria_editar, name="categoria_editar"),

    path('lugares/', views.ver_lugares, name="ver_lugares"),
    path('lugar/nuevo', views.lugar_nuevo, name="lugar_nuevo"),
    path('lugar/editar/<int:id>', views.lugar_editar, name="lugar_editar"),

    path('productos/', views.ver_productos, name="ver_productos"),
    path('producto/nuevo', views.producto_nuevo, name="producto_nuevo"),
    path('producto/editar/<int:id>', views.producto_editar, name="producto_editar"),
] 
