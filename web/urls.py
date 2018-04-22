from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('zona/', views.zonas, name="zonas"),
    path('zona/<int:id>', views.zona, name="zona"),

] 
