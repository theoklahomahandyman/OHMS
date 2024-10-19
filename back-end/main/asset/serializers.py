from asset.models import Asset, AssetInstance, AssetMaintenance
from rest_framework import serializers

# Serializer for asset model
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'name', 'description', 'notes']

# Serializer for asset instance model
class AssetInstanceSerializer(serializers.ModelSerializer):
    class  Meta:
        model = AssetInstance
        fields = ['id', 'asset', 'serial_number', 'unit_cost', 'rental_cost', 'last_maintenance', 'next_maintenance', 'usage', 'location', 'condition', 'notes']

    def validate(self, data):
        last_maintenance = data.get('last_maintenance')
        next_maintenance = data.get('next_maintenance')
        if last_maintenance and next_maintenance:
            if last_maintenance >= next_maintenance:
                raise serializers.ValidationError({'next_maintenance': 'The next maintenance date must be after the last maintenance date.'})
        return data

class AssetMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetMaintenance
        fields = ['id', 'instance', 'date', 'next_maintenance', 'current_usage', 'condition', 'notes']

    def validate(self, data):
        date = data.get('date')
        next_maintenance = data.get('next_maintenance')
        if date and next_maintenance:
            if date >= next_maintenance:
                raise serializers.ValidationError({'date': 'The next maintenance date must be after the maintenance date.'})
        return data
