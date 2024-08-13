from rest_framework import serializers
from service.models import Service

# Serializer for service model
class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ['name', 'description']
        