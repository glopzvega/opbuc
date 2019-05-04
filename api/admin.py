from django.contrib import admin

# Register your models here.
from . import models

@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
	list_display = ("id", "facebook", "twitter", "conekta_public")	

@admin.register(models.Zone)
class ZoneAdmin(admin.ModelAdmin):
	list_display = ("id", "name")	

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "tipo")	

@admin.register(models.Lugar)
class LugarAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "description", "category", "zone", "user", "sugerido", "nuevo")

@admin.register(models.Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "category", "lugar", "description", "price")

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "fecha_pedido", "hora_pedido", "usuario", "invitados", "total")

@admin.register(models.OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
	list_display = ("id", "producto", "quantity", "subtotal", "order")

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = ("id", "lugar_id", "producto_id")

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ("id", "lugar", "producto", "usuario", "fecha", "lugar")	

