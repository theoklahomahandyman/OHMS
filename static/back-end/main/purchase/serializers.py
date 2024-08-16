from purchase.models import Purchase, PurchaseMaterial
from rest_framework import serializers

# Serializer for purchase model
class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ['supplier', 'supplier_address', 'tax', 'total', 'date', 'reciept']

# Serializer for purchase material model
class PurchaseMaterialSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PurchaseMaterial
        fields = ['purchase', 'material', 'quantity', 'cost']
