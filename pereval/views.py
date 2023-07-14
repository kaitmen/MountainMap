from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *


class SubmitData(APIView):
    serializer_class = PerevalSerializer

    def get(self, request, format=None):
        """for testing"""
        perevals = Pereval.objects.all()
        serializer = PerevalSerializer(perevals, many=True)
        return Response(serializer.data)

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