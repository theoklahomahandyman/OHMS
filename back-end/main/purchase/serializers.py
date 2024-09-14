from supplier.serializers import SupplierSerializer, SupplierAddressSerializer
from purchase.models import Purchase, PurchaseMaterial
from supplier.models import Supplier, SupplierAddress
from rest_framework import serializers

# Serializer for purchase model
class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ['id', 'supplier', 'supplier_address', 'tax', 'total', 'date', 'reciept']

# Serializer for purchase material model
class PurchaseMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseMaterial
        fields = ['id', 'purchase', 'material', 'quantity', 'cost']
