from service_type.serializers import ServiceTypeSerializer
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from service_type.models import ServiceType
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for service type model
class TestServiceTypeModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.service_type = ServiceType.objects.create(name='Test')

    ## Test string method for service type model
    def test_service_type_string(self):
        self.assertEqual(str(self.service_type), self.service_type.name)

class TestServiceTypeSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.long_string = 'a' * 501
        cls.service_type = ServiceType.objects.create(name='Test', description='test service type')
        cls.empty_data = {'name': ''}
        cls.short_data = {'name': 'a'}
        cls.long_data = {'name': cls.long_string, 'description': cls.long_string}
        cls.create_data = {'name': 'name'}
        cls.update_data = {'name': 'updated', 'description': 'updated'}

    ## Test validate with empty data
    def test_validate_empty_data(self):
        serializer = ServiceTypeSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test validate with short data
    def test_validate_short_data(self):
        serializer = ServiceTypeSerializer(data=self.short_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test validate with long data
    def test_validate_long_data(self):
        serializer = ServiceTypeSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('description', serializer.errors)

    ## Test validate with existing name
    def test_validate_existing_name(self):
        self.create_data['name'] = self.service_type.name
        serializer = ServiceTypeSerializer(data=self.create_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test create success
    def test_create_success(self):
        serializer = ServiceTypeSerializer(data=self.create_data)
        self.assertTrue(serializer.is_valid())

    ## Test update success
    def test_update_success(self):
        serializer = ServiceTypeSerializer(instance= self.service_type, data=self.create_data)
        self.assertTrue(serializer.is_valid())

class TestServiceTypeView(APITestCase):
    pass
