from uuid import uuid4
from rest_framework import serializers
import base64
from django.core.files.base import ContentFile
from .models import *


def base64_to_image(base64_string):
    format, imgstr = base64_string.split(';base64,')
    ext = format.split('/')[-1]
    return ContentFile(base64.b64decode(imgstr), name=uuid4().hex + "." + ext)


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class ImagesSerializer(serializers.HyperlinkedModelSerializer):
    data = serializers.ImageField()

    class Meta:
        model = Images
        fields = ['title', 'data']


class PerevalSerializer(serializers.HyperlinkedModelSerializer):
    user = CustomUserSerializer()

    images = serializers.ListField()

    class Meta:
        model = Pereval
        fields = ['user', 'beauty_title', 'title', 'other_titles', 'connect', 'coords', 'level', 'status', 'add_time',
                  'images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop("images")
        profile_data = validated_data.pop('user')
        custom_user, created = CustomUser.objects.update_or_create(
            email=profile_data['email'],
            defaults={
                "fam": profile_data['fam'],
                "name": profile_data['name'],
                "otc": profile_data['otc'],
                "phone": profile_data['phone'],
            }
        )

        pereval = Pereval.objects.create(user=custom_user, **validated_data)

        for image in uploaded_images:
            Images.objects.create(pereval=pereval, path=base64_to_image(image['data']), title=image['title'])

        return pereval