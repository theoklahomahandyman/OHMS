from order.serializers import OrderSerializer, OrderCostSerializer, OrderPictureSerializer, OrderMaterialSerializer, OrderPaymentSerializer
from order.models import Order, OrderCost, OrderPicture, OrderMaterial, OrderPayment
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# CRUD view for order model
class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return Order.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        if pk:
            try:
                order = self.get_object(pk)
                serializer = OrderSerializer(order)
            except Order.DoesNotExist:
                return Response({'detail': 'Order Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data, partial=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

## CRUD view for order cost model

## CRUD view for order picture model

## CRUD view for order material model

## CRUD view for order payment model
