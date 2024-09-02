from rest_framework import serializers
from customer.models import Customer
import re

# Serializer for customer model
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'notes']

    def validate(self, data):
        errors = {}
        # Regular expression to match the format x (xxx) xxx-xxxx or xx (xxx) xxx-xxxx
        phone_regex = r'^\d{1,2} \(\d{3}\) \d{3}-\d{4}$'
        if 'phone' in data and not re.match(phone_regex, data['phone']):
            errors['phone'] = 'Phone number must be in the format: x (xxx) xxx-xxxx or xx (xxx) xxx-xxxx.'
        if errors:
            raise serializers.ValidationError(errors)
        return data
