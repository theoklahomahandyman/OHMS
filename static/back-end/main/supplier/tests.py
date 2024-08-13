# from supplier.serializers import SupplierSerializer, SupplierAddressSerializer
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from supplier.models import Supplier, SupplierAddress
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for supplier model
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
