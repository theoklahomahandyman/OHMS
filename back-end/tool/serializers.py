from rest_framework import serializers
from tool.models import Tool

# Serializer for tool model
class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'name', 'description', 'unit_cost', 'available_quantity']
