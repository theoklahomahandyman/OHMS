from order.models import Order, OrderCost, OrderMaterial, OrderTool, OrderPicture, OrderPayment, OrderWorkLog, OrderWorker
from rest_framework import serializers

# Serializer for order picture model
class OrderPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPicture
        fields = ['id', 'order', 'image']

# Serializer for order model
class OrderSerializer(serializers.ModelSerializer):
    images = OrderPictureSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(child = serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False), write_only=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'callout', 'date', 'description', 'service', 'hourly_rate', 'hours_worked', 'labor_total', 'material_upcharge', 'material_total', 'line_total', 'subtotal', 'tax', 'tax_total','completed', 'paid', 'discount', 'discount_total', 'total', 'payment_total', 'working_total', 'notes', 'images', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        order = Order.objects.create(**validated_data)
        for image in uploaded_images:
            OrderPicture.objects.create(order=order, image=image)
        return order

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        instance.customer = validated_data.get('customer', instance.customer)
        instance.callout = validated_data.get('callout', instance.callout)
        instance.date = validated_data.get('date', instance.date)
        instance.description = validated_data.get('description', instance.description)
        instance.service = validated_data.get('service', instance.service)
        instance.hourly_rate = validated_data.get('hourly_rate', instance.hourly_rate)
        instance.material_upcharge = validated_data.get('material_upcharge', instance.material_upcharge)
        instance.tax = validated_data.get('tax', instance.tax)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()
        for image in uploaded_images:
            OrderPicture.objects.create(order=instance, image=image)
        return instance

# Serializer for order work log model
class OrderWorkLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderWorkLog
        fields = ['id', 'order', 'start', 'end']

# Serializer for order cost model
class OrderCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCost
        fields = ['id', 'order', 'name', 'cost']

# Serializer for order material model
class OrderMaterialSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='material.name', read_only=True)

    class Meta:
        model = OrderMaterial
        fields = ['id', 'order', 'material', 'name', 'quantity']

# Serializer for order tool model
class OrderToolSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='tool.name', read_only=True)

    class Meta:
        model = OrderTool
        fields = ['id', 'order', 'tool', 'name', 'quantity_used', 'quantity_broken']

# # Serializer for order asset model
# class OrderAssetSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source='instance.asset.name', read_only=True)
#     serial_number = serializers.CharField(source='instance.serial_number', read_only=True)

#     class Meta:
#         model = OrderAsset
#         fields = ['id', 'order', 'instance', 'name', 'serial_number', 'usage', 'condition']

# Serializer for order payment model
class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = ['id', 'order', 'type', 'date', 'total', 'notes']

# Serializer for order worker model
class OrderWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderWorker
        fields = ['id', 'order', 'user', 'total']
