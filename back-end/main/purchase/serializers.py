from purchase.models import Purchase, PurchaseMaterial, PurchaseReciept
from rest_framework import serializers

# Serializer for purchase reciept model
class PurchaseRecieptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReciept
        fields = ['id', 'purchase', 'image']

# Serializer for purchase model
class PurchaseSerializer(serializers.ModelSerializer):
    images = PurchaseRecieptSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(child = serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False), write_only=True)

    class Meta:
        model = Purchase
        fields = ['id', 'supplier', 'supplier_address', 'tax', 'total', 'date', 'images', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        purchase = Purchase.objects.create(**validated_data)
        for image in uploaded_images:
            PurchaseReciept.objects.create(purchase=purchase, image=image)
        return purchase

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.supplier_address = validated_data.get('supplier_address', instance.supplier_address)
        instance.tax = validated_data.get('tax', instance.tax)
        instance.total = validated_data.get('total', instance.total)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        for image in uploaded_images:
            PurchaseReciept.objects.create(purchase=instance, image=image)
        return instance

# Serializer for purchase material model
class PurchaseMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseMaterial
        fields = ['id', 'purchase', 'material', 'quantity', 'cost']
