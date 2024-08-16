from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from purchase.serializers import PurchaseSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from purchase.models import Purchase
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

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        purchase = self.get_object(pk)
        serializer = PurchaseSerializer(purchase, data=request.data, partial=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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
