from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from supplier.models import Supplier, SupplierAddress
from django.contrib.staticfiles.finders import find
from purchase.serializers import PurchaseSerializer
from purchase.models import Purchase
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for purchase models
class TestPurchaseModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)
        cls.purchase = Purchase.objects.create(supplier=cls.supplier, supplier_address=cls.address, tax=6.83, total=6.83, date='2024-08-01', reciept='pergola-stain.jpg')

    ## Test string method for purchase model
    def test_purchase_string(self):
        self.assertEqual(str(self.purchase), f'OHMS{self.purchase.pk}-PUR')

# Tests for purchase serializer
class TestPurchaseSerializer(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.reciept = SimpleUploadedFile(name='pergola-stain.jpg', content=open(find('pergola-stain.jpg'), 'rb').read(), content_type='image/jpg')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)
        cls.purchase = Purchase.objects.create(supplier=cls.supplier, supplier_address=cls.address, tax=6.83, total=6.83, date='2024-08-01', reciept='pergola-stain.jpg')
        cls.empty_data = {'supplier': '', 'supplier_address': '', 'tax': '', 'total': '', 'date': '', 'reciept': ''}
        cls.negative_data = {'supplier': cls.supplier.pk, 'supplier_address': cls.address.pk, 'tax': -6.78, 'total': -6.78, 'date': '2024-08-01', 'reciept': cls.reciept}
        cls.valid_data = {'supplier': cls.supplier.pk, 'supplier_address': cls.address.pk, 'tax': 6.78, 'total': 6.78, 'date': '2024-08-01', 'reciept': cls.reciept}

    ## Test purchase serializer with empty data
    def test_purchase_serializer_empty_data(self):
        serializer = PurchaseSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('supplier', serializer.errors)
        self.assertIn('supplier_address', serializer.errors)
        self.assertIn('date', serializer.errors)
        self.assertIn('reciept', serializer.errors)

    ## Test purchase serializer with negative data
    def test_purchase_serializer_negative_data(self):
        serializer = PurchaseSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tax', serializer.errors)
        self.assertIn('total', serializer.errors)

    ## Test purchase serializer validation success
    def test_purchase_serializer_validation_success(self):
        serializer = PurchaseSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('supplier', serializer.validated_data)
        self.assertIn('supplier_address', serializer.validated_data)
        self.assertIn('tax', serializer.validated_data)
        self.assertIn('total', serializer.validated_data)
        self.assertIn('date', serializer.validated_data)
        self.assertIn('reciept', serializer.validated_data)
