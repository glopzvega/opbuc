from django.shortcuts import render
from rest_framework import viewsets

from django.contrib.auth.models import User, Group

from . import models
from . import serializers as s


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