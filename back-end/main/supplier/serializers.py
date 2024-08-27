from supplier.models import Supplier, SupplierAddress
from rest_framework import serializers

# Serializer for supplier model
class SupplierSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Supplier
        fields = ['name', 'notes']

# Serializer for supplier address model
class SupplierAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SupplierAddress
        fields = ['supplier', 'street_address', 'city', 'state', 'zip', 'notes']

    def validate_zip(self, value):
        if not (10000 <= value <= 99999):
            raise serializers.ValidationError('ZIP code must be exactly 5 digits.')
        return value
