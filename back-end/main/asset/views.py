from asset.serializers import AssetSerializer, AssetInstanceSerializer, AssetMaintenanceSerializer
from asset.models import Asset, AssetInstance, AssetMaintenance
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# CRUD view for asset model
class AssetView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return Asset.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        if pk:
            try:
                asset = self.get_object(pk)
                serializer = AssetSerializer(asset)
            except Asset.DoesNotExist:
                return Response({'detail': 'Asset Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            assets = Asset.objects.all()
            serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = AssetSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        asset = self.get_object(pk)
        serializer = AssetSerializer(asset, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        asset = self.get_object(pk)
        asset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CRUD view for asset insstance model
class AssetInstanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return AssetInstance.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        asset_pk = kwargs.pop('asset_pk', None)
        instance_pk = kwargs.pop('instance_pk', None)
        if instance_pk:
            try:
                asset_instance = self.get_object(instance_pk)
                serializer = AssetInstanceSerializer(asset_instance)
            except AssetInstance.DoesNotExist:
                return Response({'detail': 'Asset Instance Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            asset_instances = AssetInstance.objects.filter(asset__pk=asset_pk)
            serializer = AssetInstanceSerializer(asset_instances, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        asset_pk = kwargs.pop('asset_pk', None)
        data = request.data.copy()
        data['asset'] = asset_pk
        serializer = AssetInstanceSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('instance_pk', None)
        asset_instance = self.get_object(pk)
        serializer = AssetInstanceSerializer(asset_instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('instance_pk', None)
        asset_instance = self.get_object(pk)
        asset_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CRUD view for all asset instance model
class AllAssetInstancesView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return AssetInstance.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            asset_instances = self.get_object()
            serializer = AssetInstanceSerializer(asset_instances)
        except AssetInstance.DoesNotExist:
            return Response({'detail': 'No Asset Instances Found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

# CRUD view for asset maintenance model
class AssetMaintenanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return AssetMaintenance.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        instance_pk = kwargs.pop('instance_pk', None)
        maintenance_pk = kwargs.pop('maintenance_pk', None)
        if maintenance_pk:
            try:
                instance_maintenance = self.get_object(maintenance_pk)
                serializer = AssetMaintenanceSerializer(instance_maintenance)
            except AssetMaintenance.DoesNotExist:
                return Response({'detail': 'Asset Maintenance Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            asset_maintenances = AssetMaintenance.objects.filter(instance__pk=instance_pk)
            serializer = AssetMaintenanceSerializer(asset_maintenances, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        instance_pk = kwargs.pop('instance_pk', None)
        data = request.data.copy()
        data['instance'] = instance_pk
        serializer = AssetMaintenanceSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('maintenance_pk', None)
        instance_maintenance = self.get_object(pk)
        serializer = AssetMaintenanceSerializer(instance_maintenance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('maintenance_pk', None)
        instance_maintenance = self.get_object(pk)
        instance_maintenance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
