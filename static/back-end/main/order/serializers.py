from order.models import Order, OrderCost, OrderMaterial, OrderPicture, OrderPayment
from rest_framework import serializers

# Serializer for order model
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'callout', 'date', 'description', 'service', 'hourly_rate', 'hours_worked', 'material_upcharge', 'tax', 'total', 'completed', 'paid', 'discount', 'notes']

# Serializer for order cost model
class OrderCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCost
        fields = ['order', 'name', 'cost']

# Serializer for order material model
class OrderMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMaterial
        fields = ['order', 'material', 'quantity', 'price']

# Serializer for order picture model
class OrderPictureSerializer(serializers.ModelSerializer):
    class Meta: 
        model = OrderPicture
        fields = ['order', 'material', 'quantity', 'price']

# Serializer for order payment model
class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = ['order', 'customer', 'type', 'date', 'total', 'notes']
