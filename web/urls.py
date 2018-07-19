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
    path('pedidos/', views.ver_pedidos, name="ver_pedidos"),
    path('pedidos/<int:id>', views.detalle_pedido, name="detalle_pedido"),

    # path('lugar/<int:id>/carrito/', views.ver_carrito_lugar, name="carrito_lugar"),
    path('carrito/', views.ver_carrito, name="carrito"),
    path('carrito/comprar/', views.comprar_carrito, name="comprar_carrito"),
    path('carrito/agregar/<int:id>', views.agregar_carrito, name="agregar_carrito"),
    path('carrito/quitar/<int:id>', views.quitar_carrito, name="quitar_carrito"),
    path('carrito/qty/<int:id>', views.cantidad_carrito, name="qty_carrito"),

    # ADMIN URL
    path('categorias/', views.ver_categorias, name="ver_categorias"),
    path('categoria/nuevo', views.categoria_nuevo, name="categoria_nuevo"),
    path('categoria/editar/<int:id>', views.categoria_editar, name="categoria_editar"),

    path('lugares/', views.ver_lugares, name="ver_lugares"),
    path('lugar/nuevo', views.lugar_nuevo, name="lugar_nuevo"),
    path('lugar/editar/<int:id>', views.lugar_editar, name="lugar_editar"),
    path('lugar/<int:id>/foto/upload', views.lugar_photo_upload, name='lugar_photo_upload'),
    path('lugar/<int:id>/comment/upload', views.lugar_comment_upload, name='lugar_comment_upload'),

    path('productos/', views.ver_productos, name="ver_productos"),
    path('producto/nuevo', views.producto_nuevo, name="producto_nuevo"),
    path('producto/editar/<int:id>', views.producto_editar, name="producto_editar"),
    path('producto/<int:id>/fotos', views.producto_fotos, name="producto_fotos"),
    path('producto/<int:id>/foto/upload', views.producto_photo_upload, name='producto_photo_upload'),
    
    path('photo/<int:id>/delete', views.eliminar_foto, name="eliminar_foto"),
    path('photo/<int:id>/main', views.main_foto, name="main_foto"),


] 
