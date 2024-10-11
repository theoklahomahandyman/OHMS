from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from asset.serializers import AssetSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from asset.models import Asset

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
