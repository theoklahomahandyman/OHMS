from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from service.serializers import ServiceSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from service.models import Service
from rest_framework import status

# CRUD view for service model
class ServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return Service.objects.get(pk=pk)
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        if pk:
            try:
                service = self.get_object(pk)
                serializer = ServiceSerializer(service)
            except Service.DoesNotExist:
                return Response({'detail': 'Service Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = ServiceSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        service = self.get_object(pk)
        serializer = ServiceSerializer(service, data=request.data, partial=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        service = self.get_object(pk)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        service = self.get_object(pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
