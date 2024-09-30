from order.models import Order, OrderCost, OrderMaterial, OrderPicture, OrderPayment
from rest_framework import serializers

# Serializer for order picture model
class OrderPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPicture
        fields = ['id', 'order', 'picture']

# Serializer for order model
class OrderSerializer(serializers.ModelSerializer):
    images = OrderPictureSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(child = serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False), write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'callout', 'date', 'description', 'service', 'hourly_rate', 'hours_worked', 'material_upcharge', 'tax', 'total', 'completed', 'paid', 'discount', 'notes', 'images', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        order = Order.objects.create(**validated_data)
        for image in uploaded_images:
            OrderPicture.objects.create(order=order, image=image)
        return order

# Serializer for order cost model
class OrderCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCost
        fields = ['id', 'order', 'name', 'cost']

# Serializer for order material model
class OrderMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMaterial
        fields = ['id', 'order', 'material', 'quantity']

# Serializer for order payment model
class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = ['id', 'order', 'type', 'date', 'total', 'notes']
