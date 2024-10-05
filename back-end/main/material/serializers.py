from rest_framework import serializers
from material.models import Material

# Serializer for material model
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'description', 'size', 'unit_cost', 'available_quantity']
