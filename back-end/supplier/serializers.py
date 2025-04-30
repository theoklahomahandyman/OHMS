from supplier.models import Supplier, SupplierAddress
from rest_framework import serializers

''' Serializer for supplier address model '''
class SupplierAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierAddress
        fields = ['id', 'street_address', 'city', 'state', 'zip', 'notes']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False}
        }

    def validate_zip(self, value):
        if not (10000 <= value <= 99999):
            raise serializers.ValidationError('ZIP code must be exactly 5 digits.')
        return value

''' Serializer for supplier model '''
class SupplierSerializer(serializers.ModelSerializer):
    addresses = SupplierAddressSerializer(many=True, read_only=False)

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'notes', 'addresses']

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        supplier = Supplier.objects.create(**validated_data)
        self._process_addresses(supplier, addresses_data)
        return supplier

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        instance.name = validated_data.get('name', instance.name)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()
        self._process_addresses(instance, addresses_data)
        return instance

    def _process_addresses(self, supplier, addresses_data):
        existing_addresses = supplier.addresses.all()
        existing_ids = {a.id for a in existing_addresses}
        incoming_ids = set()
        for addr_data in addresses_data:
            addr_id = addr_data.get('id')
            if addr_id and addr_id in existing_ids:
                address = existing_addresses.get(id=addr_id)
                for key, value in addr_data.items():
                    setattr(address, key, value)
                address.save()
                incoming_ids.add(addr_id)
            else:
                addr_data.pop('id', None)
                SupplierAddress.objects.create(supplier=supplier, **addr_data)
        for address in existing_addresses:
            if address.id not in incoming_ids:
                address.delete()
