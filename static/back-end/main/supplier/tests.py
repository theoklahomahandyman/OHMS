from supplier.serializers import SupplierSerializer, SupplierAddressSerializer
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from supplier.models import Supplier, SupplierAddress
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for supplier models
class TestSupplierModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)

    ## Test string method for supplier model
    def test_supplier_string(self):
        self.assertEqual(str(self.supplier), self.supplier.name)
        
    ## Test string method for supplier address model
    def test_supplier_address_string(self):
        self.assertEqual(str(self.address), f'{self.supplier.name} - {self.address.city} - {self.address.street_address}')

# Tests for supplier serializers
class TestSupplierSerializers(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)
        cls.long_string = 'a' * 501
        cls.empty_supplier_data = {'name': ''}
        cls.short_supplier_data = {'name': 'T'}
        cls.long_supplier_data = {'name': cls.long_string, 'notes': cls.long_string}
        cls.supplier_data = {'name': 'test', 'notes': 'test notes'}
        cls.empty_supplier_address_data = {'supplier': '', 'street_address': '', 'city': '', 'state': '', 'zip': ''}
        cls.short_supplier_address_data = {'supplier': cls.supplier.pk, 'street_address': 'T', 'city': 'C', 'state': 'O', 'zip': 482}
        cls.long_supplier_address_data = {'supplier': cls.supplier.pk, 'street_address': cls.long_string, 'city': cls.long_string, 'state': cls.long_string, 'zip': 57390238573}
        cls.supplier_address_data = {'supplier': cls.supplier.pk, 'street_address': '164 Main St', 'city': 'City', 'state': 'State', 'zip': 48023}

    ## Test supplier serializer with empty data
    def test_supplier_serializer_empty_data(self):
        serializer = SupplierSerializer(data=self.empty_supplier_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
    
    ## Test supplier serializer with short data
    def test_supplier_serializer_short_data(self):
        serializer = SupplierSerializer(data=self.short_supplier_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        
    ## Test supplier serializer with long data
    def test_supplier_serializer_long_data(self):
        serializer = SupplierSerializer(data=self.long_supplier_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('notes', serializer.errors)
    
    ## Test supplier serializer validation success
    def test_supplier_serializer_validation_success(self):
        serializer = SupplierSerializer(data=self.supplier_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('name', serializer.validated_data)
        self.assertIn('notes', serializer.validated_data)

    ## Test supplier address serializer with empty data
    def test_supplier_address_serializer_empty_data(self):
        serializer = SupplierAddressSerializer(data=self.empty_supplier_address_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('supplier', serializer.errors)
        self.assertIn('street_address', serializer.errors)
        self.assertIn('city', serializer.errors)
        self.assertIn('state', serializer.errors)
        self.assertIn('zip', serializer.errors)
    
    ## Test supplier address serializer with short data
    def test_supplier_address_serializer_short_data(self):
        serializer = SupplierAddressSerializer(data=self.short_supplier_address_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('street_address', serializer.errors)
        self.assertIn('city', serializer.errors)
        self.assertIn('state', serializer.errors)
        self.assertIn('zip', serializer.errors)
        
    ## Test supplier address serializer with long data
    def test_supplier_address_serializer_long_data(self):
        serializer = SupplierAddressSerializer(data=self.long_supplier_address_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('street_address', serializer.errors)
        self.assertIn('city', serializer.errors)
        self.assertIn('state', serializer.errors)
        self.assertIn('zip', serializer.errors)
    
    ## Test supplier address serializer validation success
    def test_supplier_address_serializer_validation_success(self):
        serializer = SupplierAddressSerializer(data=self.supplier_address_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('supplier', serializer.validated_data)
        self.assertIn('street_address', serializer.validated_data)
        self.assertIn('city', serializer.validated_data)
        self.assertIn('state', serializer.validated_data)
        self.assertIn('zip', serializer.validated_data)
