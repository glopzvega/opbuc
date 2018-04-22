from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ZoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Zone
        fields = ('url', 'name', 'photo')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Category
        fields = ('url', 'name', 'photo')

class LugarSerializer(serializers.ModelSerializer):
    # photos = serializers.StringRelatedField(many=True)
    photos = serializers.HyperlinkedRelatedField(
        many=True, 
        read_only=True,
        view_name='photo-detail')
    class Meta:
        model = models.Lugar
        fields = ('url', 'name', 'category', 'zone', 'photos')

class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Photo
        fields = ('url', 'name', 'photo', 'order', 'lugar_id')