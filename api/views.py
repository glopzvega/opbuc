from django.shortcuts import render
from rest_framework import viewsets

from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView

# Imports Login forma metodo
# import warnings
# from django.utils.deprecation import RemovedInDjango21Warning
# from django.contrib.auth import (
#     REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
#     logout as auth_logout, update_session_auth_hash,
# )
# from django.contrib.auth.forms import (
#     AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
# )
###############

from . import models
from . import serializers as s

# Pass params login_image background forma ClassView 
class CustomLoginView(LoginView):
    """
    Custom login view.
    """
    def get_context_data(self, **kwargs):
        context = super(CustomLoginView, self).get_context_data(**kwargs)        
        config_ids = models.Config.objects.all()
        if config_ids:
            context.update({
                "config" : config_ids[0]
            })
        return context

# Pass params login_image background forma method
# def login(request, template_name='registration/login.html',
#           redirect_field_name=REDIRECT_FIELD_NAME,
#           authentication_form=AuthenticationForm,
#           extra_context=None, redirect_authenticated_user=False):
#     warnings.warn(
#         'The login() view is superseded by the class-based LoginView().',
#         RemovedInDjango21Warning, stacklevel=2
#     )

#     config_ids = models.Config.objects.all()
#     if config_ids:
#         extra_context.update({
#             "config" : config_ids[0]
#         })
#     return LoginView.as_view(
#         template_name=template_name,
#         redirect_field_name=redirect_field_name,
#         form_class=authentication_form,
#         extra_context=extra_context,
#         redirect_authenticated_user=redirect_authenticated_user,
#     )(request)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = s.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = s.GroupSerializer


class ZoneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Zone.objects.all()
    serializer_class = s.ZoneSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Category.objects.all()
    serializer_class = s.CategorySerializer


class LugarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Lugar.objects.all()
    serializer_class = s.LugarSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Photo.objects.all()
    serializer_class = s.PhotoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Producto.objects.all()
    serializer_class = s.ProductoSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Order.objects.all()
    serializer_class = s.OrderSerializer

class OrderLineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.OrderLine.objects.all()
    serializer_class = s.OrderLineSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Comment.objects.all()
    serializer_class = s.CommentSerializer