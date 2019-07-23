from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('signuphost/', views.signup_host, name="signup_host"),
    path('zona/', views.zonas, name="zonas"),
    path('zona/<int:id>', views.lugares_zona, name="lugares_zona"),    
    path('categoria/<int:id>', views.lugares_categoria, name="lugares_categoria"),
    path('categoria/<int:id>/zona/<int:zone_id>', views.lugares_categoria_zona, name="lugares_categoria_zona"),    
    path('lugar/<int:id>', views.lugar, name="lugar"),    
    path('buscarlugar/', views.buscarlugar, name="buscarlugar"),    
    path('producto/<int:id>', views.producto, name="producto"),
    path('pedidos/', views.ver_pedidos, name="ver_pedidos"),
    path('pedidos/<int:id>', views.detalle_pedido, name="detalle_pedido"),
    path('pedidos/validar/<int:id>', views.validar_pedido, name="validar_pedido"),
    path('pedidos/entregar/<int:id>', views.entregar_pedido, name="entregar_pedido"),
    path('pedidos/cancelar/<int:id>', views.cancelar_pedido, name="cancelar_pedido"),

    # path('lugar/<int:id>/carrito/', views.ver_carrito_lugar, name="carrito_lugar"),
    path('compra/', views.ver_carrito, name="carrito"),
    path('compra/reservar/<int:id>/', views.compra_reservar, name="compra_reservar"),
    path('compra/registrar/', views.registrar_compra, name="comprar_carrito"),
    path('compra/agregar/<int:id>', views.agregar_carrito, name="agregar_carrito"),
    path('compra/quitar/<int:id>', views.quitar_carrito, name="quitar_carrito"),
    path('compra/qty/<int:id>', views.cantidad_carrito, name="qty_carrito"),

    # ADMIN URL

    path('payment/', views.webhook_payment, name="payment"),

    path('config/', views.get_config, name="config"),
    path('mensajes/', views.get_mensajes, name="mensajes"),
    
    path('usuarios/', views.get_usuarios, name="usuarios"),
    path('usuarios/email/', views.mail_usuarios, name="mail_usuarios"),
    path('usuarios/update/<int:id>/', views.update_usuario, name="update_usuario"),
    path('usuarios/bloquear/<int:id>/', views.bloquear_usuario, name="bloquear_usuario"),
    path('usuarios/suggest/<int:id>/', views.suggest_usuario, name="suggest_usuario"),
    
    path('categorias/', views.ver_categorias, name="ver_categorias"),
    path('categoria/nuevo', views.categoria_nuevo, name="categoria_nuevo"),
    path('categoria/editar/<int:id>', views.categoria_editar, name="categoria_editar"),
    path('categorias/bloquear/<int:id>', views.categoria_bloquear, name="categoria_bloquear"),
    
    path('categoriaslugares/', views.ver_categorias_lugares, name="ver_categorias_lugares"),
    path('categorialugar/nuevo', views.categoria_lugar_nuevo, name="categoria_lugar_nuevo"),
    path('categorialugar/editar/<int:id>', views.categoria_lugar_editar, name="categoria_lugar_editar"),

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
