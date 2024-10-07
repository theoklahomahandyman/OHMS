from purchase.serializers import PurchaseSerializer, PurchaseMaterialSerializer
from purchase.models import Purchase, PurchaseMaterial, PurchaseReciept
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from material.serializers import MaterialSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from material.models import Material
from rest_framework import status

# CRUD view for purchase model
class PurchaseView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return Purchase.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        if pk:
            try:
                purchase = self.get_object(pk)
                serializer = PurchaseSerializer(purchase)
            except Purchase.DoesNotExist:
                return Response({'detail': 'Purchase Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            purchases = Purchase.objects.all()
            serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PurchaseSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        purchase = self.get_object(pk)
        serializer = PurchaseSerializer(purchase, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        purchase = self.get_object(pk)
        purchase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseRecieptView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return PurchaseReciept.objects.get(pk=pk)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        reciept = self.get_object(pk)
        reciept.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CRUD view for purchase material model
class PurchaseMaterialView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return PurchaseMaterial.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        purchase_pk = kwargs.pop('purchase_pk', None)
        material_pk = kwargs.pop('material_pk', None)
        if material_pk:
            try:
                material = self.get_object(material_pk)
                serializer = PurchaseMaterialSerializer(material)
            except PurchaseMaterial.DoesNotExist:
                return Response({'detail': 'Purchase Material Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            materials = PurchaseMaterial.objects.filter(purchase__pk=purchase_pk)
            serializer = PurchaseMaterialSerializer(materials, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        purchase_pk = kwargs.pop('purchase_pk', None)
        data = request.data.copy()
        data['purchase'] = purchase_pk
        serializer = PurchaseMaterialSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('material_pk', None)
        purchase_material = self.get_object(pk)
        serializer = PurchaseMaterialSerializer(purchase_material, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('material_pk', None)
        purchase_material = self.get_object(pk)
        purchase_material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseNewMaterialView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None, name=None):
        return PurchaseMaterial.objects.get(purchase__pk=pk, material__name=name)

    def post(self, request, *args, **kwargs):
        purchase_pk = kwargs.pop('purchase_pk', None)
        try:
            purchase_material = self.get_object(pk=purchase_pk, name=request.data['name'])
            purchase_material_data = {'quantity': request.data['quantity'], 'cost': request.data['cost']}
            serializer = PurchaseMaterialSerializer(purchase_material, data=purchase_material_data, partial=True)
        except PurchaseMaterial.DoesNotExist:
            try:
                material = Material.objects.get(name=request.data['name'])
            except Material.DoesNotExist:
                try:
                    material_data = {'name': request.data['name'], 'description': request.data['description'], 'size': request.data['size']}
                    material_serializer = MaterialSerializer(data=material_data)
                    material_serializer.is_valid(raise_exception=True)
                    material_serializer.save()
                    material = Material.objects.get(name=request.data['name'], size=request.data['size'], description=request.data['description'])
                    # material = Material.objects.create(name=request.data['name'], description=request.data['description'], size=request.data['size'])
                except ValidationError as error:
                    return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            purchase_material_data = {'purchase': purchase_pk, 'material': material.pk, 'quantity': request.data['quantity'], 'cost': request.data['cost']}
            serializer = PurchaseMaterialSerializer(data=purchase_material_data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
