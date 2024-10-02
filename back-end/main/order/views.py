from order.serializers import OrderSerializer, OrderCostSerializer, OrderMaterialSerializer, OrderPaymentSerializer, OrderWorkLogSerializer
from order.models import Order, OrderCost, OrderPicture, OrderMaterial, OrderPayment, OrderWorkLog
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from customer.serializers import CustomerSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from customer.models import Customer
from service.models import Service
from rest_framework import status

class PublicView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, email=None):
        return Customer.objects.get(email=email)

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        try:
            customer = self.get_object(email)
        except Customer.DoesNotExist:
            customer_data = {
                'first_name': request.data['last_name'],
                'last_name': request.data['first_name'],
                'email': email,
                'phone': request.data['phone'],
            }
            customer_serializer = CustomerSerializer(data=customer_data)
            try:
                customer_serializer.is_valid(raise_exception=True)
                customer = customer_serializer.save()
            except ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        try:
            service = Service.objects.get(name='New Request')
        except Service.DoesNotExist:
            service = Service.objects.create(name='New Request', description='This service type is automatically generated or added when a new request is made from the public facing website.')
        order_data = {
            'service': service.pk,
            'customer': customer.pk,
            'description': request.data['description'],
        }
        order_serializer = OrderSerializer(data=order_data)
        try:
            order_serializer.is_valid(raise_exception=True)
            order_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

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

class OrderPictureView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return OrderPicture.objects.get(pk=pk)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        picture = self.get_object(pk)
        picture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

## CRUD view for order work log model
class OrderWorkLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return OrderWorkLog.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        order_pk = kwargs.pop('order_pk', None)
        work_log_pk = kwargs.pop('work_log_pk', None)
        if work_log_pk:
            try:
                work_log = self.get_object(work_log_pk)
                serializer = OrderWorkLogSerializer(work_log)
            except OrderWorkLog.DoesNotExist:
                return Response({'detail': 'Order Work Log Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            work_logs = OrderWorkLog.objects.filter(order__pk=order_pk)
            serializer = OrderWorkLogSerializer(work_logs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        order_pk = kwargs.pop('order_pk', None)
        data = request.data.copy()
        data['order'] = order_pk
        serializer = OrderWorkLogSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('work_log_pk', None)
        work_log = self.get_object(pk)
        serializer = OrderWorkLogSerializer(work_log, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('work_log_pk', None)
        work_log = self.get_object(pk)
        work_log.delete()
        work_log.order.hours_worked = work_log.order.calculate_hours_worked()
        work_log.order.total = work_log.order.calculate_total()
        work_log.order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

## CRUD view for order cost model
class OrderCostView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return OrderCost.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        order_pk = kwargs.pop('order_pk', None)
        cost_pk = kwargs.pop('cost_pk', None)
        if cost_pk:
            try:
                cost = self.get_object(cost_pk)
                serializer = OrderCostSerializer(cost)
            except OrderCost.DoesNotExist:
                return Response({'detail': 'Order Cost Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            costs = OrderCost.objects.filter(order__pk=order_pk)
            serializer = OrderCostSerializer(costs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        order_pk = kwargs.pop('order_pk', None)
        data = request.data.copy()
        data['order'] = order_pk
        serializer = OrderCostSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('cost_pk', None)
        cost = self.get_object(pk)
        serializer = OrderCostSerializer(cost, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('cost_pk', None)
        cost = self.get_object(pk)
        cost.delete()
        cost.order.total = cost.order.calculate_total()
        cost.order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

## CRUD view for order material model
class OrderMaterialView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return OrderMaterial.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        order_pk = kwargs.pop('order_pk', None)
        material_pk = kwargs.pop('material_pk', None)
        if material_pk:
            try:
                material = self.get_object(material_pk)
                serializer = OrderMaterialSerializer(material)
            except OrderMaterial.DoesNotExist:
                return Response({'detail': 'Order Material Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            materials = OrderMaterial.objects.filter(order__pk=order_pk)
            serializer = OrderMaterialSerializer(materials, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        order_pk = kwargs.pop('order_pk', None)
        data = request.data.copy()
        data['order'] = order_pk
        serializer = OrderMaterialSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('material_pk', None)
        material = self.get_object(pk)
        serializer = OrderMaterialSerializer(material, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('material_pk', None)
        material = self.get_object(pk)
        material.delete()
        material.order.total = material.order.calculate_total()
        material.order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

## CRUD view for order payment model
class OrderPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return OrderPayment.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        order_pk = kwargs.pop('order_pk', None)
        payment_pk = kwargs.pop('payment_pk', None)
        if payment_pk:
            try:
                payment = self.get_object(payment_pk)
                serializer = OrderPaymentSerializer(payment)
            except OrderPayment.DoesNotExist:
                return Response({'detail': 'Order Payment Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            payments = OrderPayment.objects.filter(order__pk=order_pk)
            serializer = OrderPaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        order_pk = kwargs.pop('order_pk', None)
        data = request.data.copy()
        data['order'] = order_pk
        serializer = OrderPaymentSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('payment_pk', None)
        payment = self.get_object(pk)
        serializer = OrderPaymentSerializer(payment, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('payment_pk', None)
        payment = self.get_object(pk)
        payment.delete()
        payment.order.determine_paid()
        return Response(status=status.HTTP_204_NO_CONTENT)
