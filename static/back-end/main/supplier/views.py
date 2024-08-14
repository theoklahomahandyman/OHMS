from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from supplier.serializers import SupplierSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from supplier.models import Supplier
from rest_framework import status

# CRUD view for supplier model
class SupplierView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return Supplier.objects.get(pk=pk)
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        if pk:
            try:
                supplier = self.get_object(pk)
                serializer = SupplierSerializer(supplier)
            except Supplier.DoesNotExist:
                return Response({'detail': 'Supplier Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            suppliers = Supplier.objects.all()
            serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = SupplierSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        supplier = self.get_object(pk)
        serializer = SupplierSerializer(supplier, data=request.data, partial=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        supplier = self.get_object(pk)
        serializer = SupplierSerializer(supplier, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        supplier = self.get_object(pk)
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
