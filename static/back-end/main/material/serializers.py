from material.models import Material, MaterialPurchase
from rest_framework import serializers

# Serializer for material model
class MaterialSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Material
        fields = ['name', 'description', 'size', 'unit_cost', 'available_quantity', 'supplier']

# SerializerMaterialPurchase for material purchase model
class MaterialPurchaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MaterialPurchase
        fields = ['material', 'purchase_quantity', 'purchase_cost', 'purchase_date', 'supplier_address']
