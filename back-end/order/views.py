from order.serializers import OrderSerializer, OrderCostSerializer, OrderMaterialSerializer, OrderToolSerializer, OrderPaymentSerializer, OrderWorkLogSerializer, OrderWorkerSerializer
from order.models import Order, OrderCost, OrderPicture, OrderMaterial, OrderTool, OrderPayment, OrderWorkLog, OrderWorker
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from customer.serializers import CustomerSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from customer.models import Customer
from service.models import Service
from rest_framework import status

''' View for public site contact form '''
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
            'date': request.data['date'],
            'description': request.data['description'],
            'notes': '',
        }
        order_serializer = OrderSerializer(data=order_data)
        try:
            order_serializer.is_valid(raise_exception=True)
            order_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

''' CRUD view for order model '''
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

''' View for order picture model '''
class OrderPictureView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return OrderPicture.objects.get(pk=pk)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        picture = self.get_object(pk)
        picture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

''' CRUD view for order work log model '''
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
        return Response(status=status.HTTP_204_NO_CONTENT)

''' CRUD view for order cost model '''
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
        return Response(status=status.HTTP_204_NO_CONTENT)

''' CRUD view for order material model '''
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
        return Response(status=status.HTTP_204_NO_CONTENT)

''' CRUD view for order tool model '''
class OrderToolView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return OrderTool.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        order_pk = kwargs.pop('order_pk', None)
        tool_pk = kwargs.pop('tool_pk', None)
        if tool_pk:
            try:
                tool = self.get_object(tool_pk)
                serializer = OrderToolSerializer(tool)
            except OrderTool.DoesNotExist:
                return Response({'detail': 'Order Tool Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            tools = OrderTool.objects.filter(order__pk=order_pk)
            serializer = OrderToolSerializer(tools, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        order_pk = kwargs.pop('order_pk', None)
        data = request.data.copy()
        data['order'] = order_pk
        serializer = OrderToolSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('tool_pk', None)
        tool = self.get_object(pk)
        serializer = OrderToolSerializer(tool, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('tool_pk', None)
        tool = self.get_object(pk)
        tool.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

''' CRUD view for order asset model '''
# class OrderAssetView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk=None):
#         return OrderAsset.objects.get(pk=pk)

#     def get(self, request, *args, **kwargs):
#         order_pk = kwargs.pop('order_pk', None)
#         asset_pk = kwargs.pop('asset_pk', None)
#         if asset_pk:
#             try:
#                 asset = self.get_object(asset_pk)
#                 serializer = OrderAssetSerializer(asset)
#             except OrderAsset.DoesNotExist:
#                 return Response({'detail': 'Order Asset Not Found.'}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             assets = OrderAsset.objects.filter(order__pk=order_pk)
#             serializer = OrderAssetSerializer(assets, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         order_pk = kwargs.pop('order_pk', None)
#         data = request.data.copy()
#         data['order'] = order_pk
#         serializer = OrderAssetSerializer(data=data)
#         try:
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except ValidationError as error:
#             return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, *args, **kwargs):
#         pk = kwargs.get('asset_pk', None)
#         asset = self.get_object(pk)
#         serializer = OrderAssetSerializer(asset, data=request.data, partial=True)
#         try:
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except ValidationError as error:
#             return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('asset_pk', None)
#         asset = self.get_object(pk)
#         asset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

''' CRUD view for order payment model '''
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
        return Response(status=status.HTTP_204_NO_CONTENT)

''' CRUD view for order worker model '''
class OrderWorkerView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return OrderWorker.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        order_pk = kwargs.pop('order_pk', None)
        worker_pk = kwargs.pop('worker_pk', None)
        if worker_pk:
            try:
                worker = self.get_object(worker_pk)
                serializer = OrderWorkerSerializer(worker)
            except OrderWorker.DoesNotExist:
                return Response({'detail': 'Order Worker Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            workers = OrderWorker.objects.filter(order__pk=order_pk)
            serializer = OrderWorkerSerializer(workers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        order_pk = kwargs.pop('order_pk', None)
        data = request.data.copy()
        data['order'] = order_pk
        serializer = OrderWorkerSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('worker_pk', None)
        worker = self.get_object(pk)
        serializer = OrderWorkerSerializer(worker, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('worker_pk', None)
        worker = self.get_object(pk)
        worker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
