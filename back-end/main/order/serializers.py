from order.models import Order, OrderCost, OrderMaterial, OrderPicture, OrderPayment
from rest_framework import serializers

# Serializer for order model
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'callout', 'date', 'description', 'service', 'hourly_rate', 'hours_worked', 'material_upcharge', 'tax', 'total', 'completed', 'paid', 'discount', 'notes']

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

# Serializer for order picture model
class OrderPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPicture
        fields = ['id', 'order', 'image']

# Serializer for order payment model
class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = ['id', 'order', 'type', 'date', 'total', 'notes']
