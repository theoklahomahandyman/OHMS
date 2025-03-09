from purchase.models import Purchase, PurchaseMaterial, PurchaseReceipt, PurchaseTool
from rest_framework import serializers

''' Serializer for purchase receipt model '''
class PurchaseReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReceipt
        fields = ['id', 'purchase', 'image']

''' Serializer for purchase material model '''
class PurchaseMaterialSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='inventory_item.name', read_only=True)

    class Meta:
        model = PurchaseMaterial
        fields = ['id', 'purchase', 'inventory_item', 'name', 'quantity', 'cost']

''' Serializer for purchase tool model '''
class PurchaseToolSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='inventory_item.name', read_only=True)

    class Meta:
        model = PurchaseTool
        fields = ['id', 'purchase', 'inventory_item', 'name', 'quantity', 'cost']

# class PurchaseAssetSerializer(serializers.ModelSerializer):
#     asset = serializers.CharField(source='instance.asset', read_only=True)
#     asset_name = serializers.CharField(source='instance.asset.name', read_only=True)
#     serial_number = serializers.CharField(source='instance.serial_number', read_only=True)
#     charge = serializers.FloatField(source='instance.rental_cost', read_only=True)
#     last_maintenance = serializers.DateField(source='instance.last_maintenance', read_only=True)
#     next_maintenance = serializers.DateField(source='instance.next_maintenance', read_only=True)

#     class Meta:
#         model = PurchaseAsset
#         fields = ['id', 'purchase', 'instance', 'asset', 'asset_name', 'serial_number', 'cost', 'charge', 'last_maintenance', 'next_maintenance', 'usage', 'condition']

''' Serializer for purchase model '''
class PurchaseSerializer(serializers.ModelSerializer):
    images = PurchaseReceiptSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(child = serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False), write_only=True)
    materials = PurchaseMaterialSerializer(many=True, read_only=True)
    tools = PurchaseToolSerializer(many=True, read_only=True)
    # assets = PurchaseAssetSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = ['id', 'supplier', 'supplier_address', 'tax', 'material_total', 'tool_total', 'subtotal', 'total', 'date', 'images', 'uploaded_images', 'materials', 'tools']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        purchase = Purchase.objects.create(**validated_data)
        for image in uploaded_images:
            PurchaseReceipt.objects.create(purchase=purchase, image=image)
        return purchase

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.supplier_address = validated_data.get('supplier_address', instance.supplier_address)
        instance.tax = validated_data.get('tax', instance.tax)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        for image in uploaded_images:
            PurchaseReceipt.objects.create(purchase=instance, image=image)
        return instance
