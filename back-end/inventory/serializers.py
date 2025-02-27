from inventory.models import Material, Tool
from rest_framework import serializers

''' Serializer for material model '''
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'description', 'size', 'available_quantity', 'unit_cost']

''' Serializer for tool model '''
class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'name', 'description', 'available_quantity', 'unit_cost']
