from asset.models import Asset, AssetMaintenance
from rest_framework import serializers

# Serializer for asset model
class AssetSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Asset
        fields = ['id', 'name', 'serial_number', 'description', 'unit_cost', 'rental_cost', 'last_maintenance', 'next_maintenance', 'usage', 'location', 'condition', 'status', 'notes']

    def validate(self, data):
        if data.get('last_maintenance') >= data.get('next_maintenance'):
            raise serializers.ValidationError({'next_maintenance': 'The next maintenance date must be after the last maintenance date.'})
        return data

class AssetMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetMaintenance
        fields = ['id', 'asset', 'date', 'next_maintenance', 'current_usage', 'condition', 'status', 'notes']

    def validate(self, data):
        if data.get('date') >= data.get('next_maintenance'):
            raise serializers.ValidationError({'date': 'The next maintenance date must be after the maintenance date.'})
        return data
