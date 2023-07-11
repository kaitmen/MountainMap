from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class PerevalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pereval
        fields = ['user', 'beauty_title', 'title', 'other_titles', 'connect', 'coords', 'level', 'status']


class ImagesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Images
        fields = ['pereval', 'title', 'path']