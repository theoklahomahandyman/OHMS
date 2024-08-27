from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from customer.serializers import CustomerSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from customer.models import Customer
from rest_framework import status

class CustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        customer = Customer.objects.get(pk=pk)
        return customer
        
    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        if pk:
            try:
                customer = self.get_object(pk)
                serializer = CustomerSerializer(customer)
            except Customer.DoesNotExist:
                return Response({'detail': 'Customer Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=False)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
