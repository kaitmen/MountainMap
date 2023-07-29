import base64
from uuid import uuid4
from rest_framework import serializers
from rest_framework import exceptions
from django.core.files.base import ContentFile

from .import StatusNames
from .models import *


def base64_to_image(base64_string):
    format, imgstr = base64_string.split(';base64,')
    ext = format.split('/')[-1]
    return ContentFile(base64.b64decode(imgstr), name=uuid4().hex + "." + ext)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ['title', 'path']


class PerevalSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    coords = CoordsSerializer()
    images = serializers.ListField()
    # level = serializers.SerializerMethodField('get_level')

    level = serializers.DictField(child=serializers.CharField(allow_blank=True), allow_null=True)

    class Meta:
        model = Pereval
        fields = ['user', 'beauty_title', 'title', 'other_titles', 'connect', 'coords', 'level',
                  'status', 'add_time', 'images']

    def get_level(self, obj):
        return {
                'winter': obj.winter,
                'summer': obj.summer,
                'autumn': obj.autumn,
                'spring': obj.spring,
            }

    def create(self, validated_data):
        uploaded_images = validated_data.pop("images")
        profile_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        levels_data = validated_data.pop('level')

        custom_user, created = CustomUser.objects.update_or_create(
            email=profile_data['email'],
            defaults={
                "fam": profile_data['fam'],
                "name": profile_data['name'],
                "otc": profile_data['otc'],
                "phone": profile_data['phone'],
            }
        )

        coords, created = Coords.objects.update_or_create(
            latitude=coords_data['latitude'],
            longitude=coords_data['longitude'],
            height=coords_data['height'],
        )

        pereval = Pereval.objects.create(
            user=custom_user,
            coords=coords,
            winter=levels_data['winter'],
            summer=levels_data['summer'],
            autumn=levels_data['autumn'],
            spring=levels_data['spring'],
            **validated_data
        )

        for image in uploaded_images:
            Images.objects.create(pereval=pereval, path=base64_to_image(image['data']), title=image['title'])

        return pereval


class DetailPerevalSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    images = ImagesSerializer(many=True, read_only=True)
    coords = CoordsSerializer()
    level = serializers.SerializerMethodField('get_level')

    class Meta:
        model = Pereval
        fields = ['user', 'beauty_title', 'title', 'other_titles', 'connect', 'coords',
                  'level', 'status', 'add_time', 'images']

    def get_level(self, obj):
        return {
                'winter': obj.winter,
                'summer': obj.summer,
                'autumn': obj.autumn,
                'spring': obj.spring,
            }


class UpdatePerevalSerializer(serializers.HyperlinkedModelSerializer):
    coords = CoordsSerializer()
    images = serializers.ListField()
    level = serializers.DictField(child=serializers.CharField(allow_blank=True), allow_null=True)

    class Meta:
        model = Pereval
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'coords', 'level',
                  'winter', 'summer', 'autumn', 'spring', 'status', 'add_time', 'images']

    def validate(self, data):
        instance = self.instance
        if instance.status == StatusNames.NEW:
            raise exceptions.ValidationError(detail="You can edit only new perevals")
        return data

    def update(self, instance, validated_data):

        coords_data = validated_data.pop('coords')
        levels_data = validated_data.pop('level')

        coords, created = Coords.objects.update_or_create(
            latitude=coords_data['latitude'],
            longitude=coords_data['longitude'],
            height=coords_data['height'],
        )

        instance.coords = coords
        instance.beauty_title = self.context['beauty_title']
        instance.title = self.context['title']
        instance.other_titles = self.context['other_titles']
        instance.connect = self.context['connect']
        instance.winter = levels_data['winter']
        instance.summer = levels_data['summer']
        instance.autumn = levels_data['autumn']
        instance.spring = levels_data['spring']
        instance.status = self.context['status']
        instance.save()

        uploaded_images = validated_data.pop("images")
        for image in uploaded_images:
            Images.objects.create(pereval=instance, path=base64_to_image(image['data']), title=image['title'])

        return instance
