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
class OrderCostView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return OrderCost.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        type = kwargs.pop('type', None)
        if type == 's':
            try:
                cost = self.get_object(pk)
                serializer = OrderCostSerializer(cost)
            except OrderCost.DoesNotExist:
                return Response({'detail': 'Order Cost Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            costs = OrderCost.objects.filter(order__pk=pk)
            serializer = OrderCostSerializer(costs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OrderCostSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        cost = self.get_object(pk)
        serializer = OrderCostSerializer(cost, data=request.data, partial=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        cost = self.get_object(pk)
        serializer = OrderCostSerializer(cost, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        cost = self.get_object(pk)
        cost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

## CRUD view for order picture model
class OrderPictureView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return OrderPicture.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        type = kwargs.pop('type', None)
        if type == 's':
            try:
                picture = self.get_object(pk)
                serializer = OrderPictureSerializer(picture)
            except OrderPicture.DoesNotExist:
                return Response({'detail': 'Order Picture Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            pictures = OrderPicture.objects.filter(order__pk=pk)
            serializer = OrderPictureSerializer(pictures, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OrderPictureSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        picture = self.get_object(pk)
        serializer = OrderPictureSerializer(picture, data=request.data, partial=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        picture = self.get_object(pk)
        serializer = OrderPictureSerializer(picture, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        picture = self.get_object(pk)
        picture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

## CRUD view for order material model
class OrderMaterialView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return OrderMaterial.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        type = kwargs.pop('type', None)
        if type == 's':
            try:
                material = self.get_object(pk)
                serializer = OrderMaterialSerializer(material)
            except OrderMaterial.DoesNotExist:
                return Response({'detail': 'Order Material Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            materials = OrderMaterial.objects.filter(order__pk=pk)
            serializer = OrderMaterialSerializer(materials, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OrderMaterialSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        material = self.get_object(pk)
        serializer = OrderMaterialSerializer(material, data=request.data, partial=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        material = self.get_object(pk)
        serializer = OrderMaterialSerializer(material, data=request.data, partial=True)
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

## CRUD view for order payment model
class OrderPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return OrderPayment.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        type = kwargs.pop('type', None)
        if type == 's':
            try:
                payment = self.get_object(pk)
                serializer = OrderPaymentSerializer(payment)
            except OrderPayment.DoesNotExist:
                return Response({'detail': 'Order Payment Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            payments = OrderPayment.objects.filter(order__pk=pk)
            serializer = OrderPaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OrderPaymentSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        payment = self.get_object(pk)
        serializer = OrderPaymentSerializer(payment, data=request.data, partial=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        payment = self.get_object(pk)
        serializer = OrderPaymentSerializer(payment, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        payment = self.get_object(pk)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
