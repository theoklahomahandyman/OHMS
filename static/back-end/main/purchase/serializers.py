from rest_framework import serializers
from purchase.models import Purchase

# Serializer for purchase model
class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ['supplier', 'supplier_address', 'tax', 'total', 'date', 'reciept']
        