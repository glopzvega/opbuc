from django.contrib import admin

# Register your models here.
from . import models

@admin.register(models.Zone)
class ZoneAdmin(admin.ModelAdmin):
	list_display = ("id", "name")	

@admin.register(models.Category)
class ZoneAdmin(admin.ModelAdmin):
	list_display = ("id", "name")	

@admin.register(models.Lugar)
class LugarAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "category", "zone")

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = ("id", "lugar_id")	

