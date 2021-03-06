"""turismo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework import routers
from api import views
from web import views as web_views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)
router.register('zones', views.ZoneViewSet)
router.register('categories', views.CategoryViewSet)
router.register('lugares', views.LugarViewSet)
router.register('photos', views.PhotoViewSet)
router.register('productos', views.ProductoViewSet)
router.register('orders', views.OrderViewSet)
router.register('order_lines', views.OrderLineViewSet)
router.register('comentarios', views.CommentViewSet)

urlpatterns = [
    path('', include('web.urls')),
    path('login/', views.CustomLoginView.as_view(), name="login"), 
    # path('login/', views.login, {"extra_context" : {}}, name="login"), 
    path('auth/', include('social_django.urls', namespace='social')),   
    # path('logingoogle/', web_views.login_google, name="login_google"),    
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'), 
	path('api/auth/', include('rest_framework.urls', namespace="rest_framework")),
	path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
