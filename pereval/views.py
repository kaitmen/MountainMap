from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *


class SubmitData(APIView):
    def get(self, request, format=None):
        """for testing"""
        perevals = Pereval.objects.all()
        serializer = PerevalSerializer(perevals, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user_serializer = CustomUserSerializer(data=request.data)
        pereval_serializer = PerevalSerializer(data=request.data)
        image_serializer = ImagesSerializer(data=request.data)

        if pereval_serializer.is_valid():
            pereval_serializer.save()
            return Response(pereval_serializer.data.id, status=status.HTTP_201_CREATED)
        return Response(pereval_serializer.errors, status=status.HTTP_400_BAD_REQUEST)