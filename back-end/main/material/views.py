from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from material.serializers import MaterialSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from material.models import Material
from rest_framework import status

# CRUD view for material model
class MaterialView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return Material.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        if pk:
            try:
                material = self.get_object(pk)
                serializer = MaterialSerializer(material)
            except Material.DoesNotExist:
                return Response({'detail': 'Material Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            materials = Material.objects.all()
            serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = MaterialSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        material = self.get_object(pk)
        serializer = MaterialSerializer(material, data=request.data, partial=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        material = self.get_object(pk)
        serializer = MaterialSerializer(material, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        material = self.get_object(pk)
        material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
