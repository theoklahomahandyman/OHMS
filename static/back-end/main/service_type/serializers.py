from service_type.models import ServiceType
from rest_framework import serializers

# Serializer for service type model
class ServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceType
        fields = ['name', 'description']
        