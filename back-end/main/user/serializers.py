from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from user.models import User

# Serializer for user model
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        errors = {}
        if 'password' in data:
            if data['password'] != data['confirm_password']:
                errors['confirm_password'] = 'Please ensure the password and confirm password fields are matching.'
            elif len(data['password']) < 8:
                errors['password'] = 'Please ensure the password is a minimum length of 8 characters.'
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        user = User.objects.create(first_name=validated_data['first_name'], last_name=validated_data['last_name'], phone=validated_data['phone'], email=validated_data['email'], password=make_password(validated_data['password']))
        return user

    def update(self, instance, validated_data):
        errors = {}
        if 'password' in validated_data:
            password = validated_data['password']
            user_info = [instance.first_name, instance.last_name, instance.email, instance.phone]
            for info in user_info:
                if any(info[i:i+4].lower() in password.lower() for i in range(len(info) - 2)):
                    errors['password'] = 'Please ensure the passwords is not too similar to your personal information.'
                    break
            if errors:
                raise serializers.ValidationError(errors)
            instance.password = make_password(validated_data['password'])
        for attr, value in validated_data.items():
            if attr not in ['password', 'confirm_password']:
                setattr(instance, attr, value)
        instance.save()
        return instance
