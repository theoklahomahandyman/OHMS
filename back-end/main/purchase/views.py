from purchase.serializers import PurchaseSerializer, PurchaseMaterialSerializer, PurchaseToolSerializer
from purchase.models import Purchase, PurchaseMaterial, PurchaseReciept, PurchaseTool
# from asset.serializers import AssetSerializer, AssetInstanceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from material.serializers import MaterialSerializer
# from asset.models import Asset, AssetInstance
from rest_framework.response import Response
from tool.serializers import ToolSerializer
from rest_framework.views import APIView
from material.models import Material
from rest_framework import status
from tool.models import Tool

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

# CRUD view for purchase tool model
class PurchaseToolView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return PurchaseTool.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        purchase_pk = kwargs.pop('purchase_pk', None)
        tool_pk = kwargs.pop('tool_pk', None)
        if tool_pk:
            try:
                tool = self.get_object(tool_pk)
                serializer = PurchaseToolSerializer(tool)
            except PurchaseTool.DoesNotExist:
                return Response({'detail': 'Purchase Tool Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            tools = PurchaseTool.objects.filter(purchase__pk=purchase_pk)
            serializer = PurchaseToolSerializer(tools, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        purchase_pk = kwargs.pop('purchase_pk', None)
        data = request.data.copy()
        data['purchase'] = purchase_pk
        serializer = PurchaseToolSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('tool_pk', None)
        purchase_tool = self.get_object(pk)
        serializer = PurchaseToolSerializer(purchase_tool, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('tool_pk', None)
        purchase_tool = self.get_object(pk)
        purchase_tool.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseNewToolView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None, name=None):
        return PurchaseTool.objects.get(purchase__pk=pk, tool__name=name)

    def post(self, request, *args, **kwargs):
        purchase_pk = kwargs.pop('purchase_pk', None)
        try:
            purchase_tool = self.get_object(pk=purchase_pk, name=request.data['name'])
            purchase_tool_data = {'quantity': request.data['quantity'], 'cost': request.data['cost']}
            serializer = PurchaseToolSerializer(purchase_tool, data=purchase_tool_data, partial=True)
        except PurchaseTool.DoesNotExist:
            try:
                tool = Tool.objects.get(name=request.data['name'])
            except Tool.DoesNotExist:
                try:
                    tool_data = {'name': request.data['name'], 'description': request.data['description']}
                    tool_serializer = ToolSerializer(data=tool_data)
                    tool_serializer.is_valid(raise_exception=True)
                    tool_serializer.save()
                    tool = Tool.objects.get(name=request.data['name'], description=request.data['description'])
                except ValidationError as error:
                    return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            purchase_tool_data = {'purchase': purchase_pk, 'tool': tool.pk, 'quantity': request.data['quantity'], 'cost': request.data['cost']}
            serializer = PurchaseToolSerializer(data=purchase_tool_data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

# # CRUD view for purchase asset model
# class PurchaseAssetView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk=None):
#         return PurchaseAsset.objects.get(pk=pk)

#     def get(self, request, *args, **kwargs):
#         purchase_pk = kwargs.pop('purchase_pk', None)
#         asset_pk = kwargs.pop('asset_pk', None)
#         if asset_pk:
#             try:
#                 purchase_asset = self.get_object(asset_pk)
#                 serializer = PurchaseAssetSerializer(purchase_asset)
#             except PurchaseAsset.DoesNotExist:
#                 return Response({'detail': 'Purchase Asset Not Found.'}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             purchase_assets = PurchaseAsset.objects.filter(purchase__pk=purchase_pk)
#             serializer = PurchaseAssetSerializer(purchase_assets, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         purchase_pk = kwargs.pop('purchase_pk', None)
#         instance_data = {'asset': request.data['asset'], 'serial_number': request.data['serial_number'], 'unit_cost': request.data['cost'], 'rental_cost': request.data['charge'], 'last_maintenance': request.data['last_maintenance'], 'next_maintenance': request.data['next_maintenance'], 'usage': request.data['usage'], 'condition': request.data['condition']}
#         instance_serializer = AssetInstanceSerializer(data=instance_data)
#         try:
#             instance_serializer.is_valid(raise_exception=True)
#             instance_serializer.save()
#             instance = AssetInstance.objects.get(serial_number=request.data['serial_number'])
#             data = {'purchase': purchase_pk, 'instance': instance.pk, 'usage': request.data['usage'], 'condition': request.data['condition'], 'cost': request.data['cost']}
#             serializer = PurchaseAssetSerializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except ValidationError as error:
#             return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, *args, **kwargs):
#         pk = kwargs.get('asset_pk', None)
#         purchase_asset = self.get_object(pk)
#         serializer = PurchaseAssetSerializer(purchase_asset, data=request.data, partial=True)
#         try:
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except ValidationError as error:
#             return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('asset_pk', None)
#         purchase_asset = self.get_object(pk)
#         purchase_asset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class PurchaseNewAssetView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk=None, name=None, serial_number=None):
#         return PurchaseAsset.objects.get(purchase__pk=pk, instance__asset__name=name, instance__serial_number=serial_number)

#     def post(self, request, *args, **kwargs):
#         purchase_pk = kwargs.pop('purchase_pk', None)
#         name = request.data.get('name', None)
#         serial_number = request.data.get('serial_number', None)
#         try:
#             purchase_asset = self.get_object(pk=purchase_pk, name=name, serial_number=serial_number)
#             purchase_asset_data = {'instance': purchase_asset.instance.pk, 'cost': request.data['cost'], 'usage': request.data['usage'], 'condition': request.data['condition']}
#             serializer = PurchaseAssetSerializer(purchase_asset, data=purchase_asset_data, partial=True)
#         except PurchaseAsset.DoesNotExist:
#             try:
#                 asset = Asset.objects.get(name=name)
#             except Asset.DoesNotExist:
#                 try:
#                     asset_data = {'name': name, 'description': request.data['description']}
#                     asset_serializer = AssetSerializer(data=asset_data)
#                     asset_serializer.is_valid(raise_exception=True)
#                     asset_serializer.save()
#                     asset = Asset.objects.get(name=name, description=request.data['description'])
#                     instance_data = {'asset': asset.pk, 'serial_number': request.data['serial_number'], 'unit_cost': request.data['cost'], 'rental_cost': request.data['charge'], 'last_maintenance': request.data['last_maintenance'], 'next_maintenance': request.data['next_maintenance'], 'usage': request.data['usage'], 'condition': request.data['condition']}
#                     instance_serializer = AssetInstanceSerializer(data=instance_data)
#                     instance_serializer.is_valid(raise_exception=True)
#                     instance_serializer.save()
#                     instance = AssetInstance.objects.get(asset=asset, serial_number=request.data['serial_number'])
#                     purchase_asset_data = {'purchase': purchase_pk, 'instance': instance.pk, 'cost': request.data['cost'], 'charge': request.data['charge'], 'usage': request.data['usage'], 'condition': request.data['condition']}
#                     serializer = PurchaseAssetSerializer(data=purchase_asset_data)
#                     serializer.is_valid(raise_exception=True)
#                     serializer.save()
#                 except ValidationError as error:
#                     return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_201_CREATED)
