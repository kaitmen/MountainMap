from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .serializers import *
from .models import *


class SubmitData(APIView):
    serializer_class = PerevalSerializer

    def get(self, request, format=None):
        try:
            email = request.GET['user__email']
            perevals = Pereval.objects.filter(user__email=email)
        except Exception as e:
            perevals = Pereval.objects.all()

        try:
            serializer = DetailPerevalSerializer(perevals, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)})

    def post(self, request, format=None):
        pereval_serializer = PerevalSerializer(data=request.data)

        try:
            if pereval_serializer.is_valid():
                object = pereval_serializer.save()
            else:
                return Response({'message': pereval_serializer.errors, 'id': None, 'status': status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': e, 'id': None, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': None, 'id': object.id, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


class DetailData(APIView):
    serializer_class = PerevalSerializer

    def get_object(self, pk):
        try:
            return Pereval.objects.get(pk=pk)
        except Pereval.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        pereval = self.get_object(id)
        serializer = DetailPerevalSerializer(pereval, many=False)
        return Response({**serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        pereval = self.get_object(id)
        serializer = UpdatePerevalSerializer(instance=pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'state': 1, 'message': None})
        return Response({'state': 0, 'message': serializer.errors})
