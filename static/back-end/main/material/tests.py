from material.serializers import MaterialSerializer, MaterialPurchaseSerializer
from rest_framework.test import APITestCase, APIClient
from material.models import Material, MaterialPurchase
from django.contrib.auth.hashers import make_password
from supplier.models import Supplier, SupplierAddress
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for material models
class TestMaterialModels(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)
        cls.material = Material.objects.create(name='material', size='2 inch X 4 inch X 8 feet', supplier=cls.supplier)

    ## Test string method for material model
    def test_material_string(self):
        self.assertEqual(str(self.material), f'{self.material.name} - {self.material.size} - {self.supplier.name}')

    ## Test save method for material purchase model with quantity of 0
    def test_material_purchase_save_quantity_0(self):
        MaterialPurchase.objects.create(material=self.material, supplier_address=self.address, purchase_quantity=0, purchase_cost=0, purchase_date='2024-08-01')
        self.material.refresh_from_db()
        self.assertEqual(self.material.unit_cost, 0.0)
        self.assertEqual(self.material.available_quantity, 0)

    ## Test save method for material purchase model
    def test_material_purchase_save(self):
        material_purchase = MaterialPurchase.objects.create(material=self.material, supplier_address=self.address, purchase_quantity=3, purchase_cost=56.32, purchase_date='2024-08-01')
        self.material.refresh_from_db()
        expected_unit_cost = material_purchase.purchase_cost / material_purchase.purchase_quantity
        self.assertEqual(self.material.unit_cost, expected_unit_cost)
        self.assertEqual(self.material.available_quantity, material_purchase.purchase_quantity)

    ## Test string method for material purchase model
    def test_material_purchase_string(self):
        material_purchase = MaterialPurchase.objects.create(material=self.material, supplier_address=self.address, purchase_quantity=3, purchase_cost=56.32, purchase_date='2024-08-01')
        self.assertEqual(str(material_purchase), f'{self.material.name} - {material_purchase.purchase_quantity} units purchased')

class TestMaterialSerializers(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)
        cls.material = Material.objects.create(name='material', size='2 inch X 4 inch X 8 feet', supplier=cls.supplier)
        cls.long_string = 'a' * 501
        cls.empty_material_data = {'name': '', 'size': '', 'supplier': ''}
        cls.short_material_data = {'name': 'T', 'size': 'S', 'supplier': cls.supplier.pk}
        cls.long_material_data = {'name': cls.long_string, 'size': cls.long_string, 'supplier': cls.supplier.pk}
        cls.material_data = {'name': 'material test', 'size': 'material size', 'supplier': cls.supplier.pk}
        cls.empty_material_purchase_data = {'material': '', 'supplier_address': '', 'purchase_quantity': '', 'purchase_cost': '', 'purchase_date': ''}
        cls.material_purchase_data = {'material': cls.material.pk, 'supplier_address': cls.address.pk, 'purchase_quantity': 3, 'purchase_cost': 45.78, 'purchase_date': '2024-08-01'}

    ## Test material serializer with empty data
    def test_material_serializer_empty_data(self):
        serializer = MaterialSerializer(data=self.empty_material_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('size', serializer.errors)
        self.assertIn('supplier', serializer.errors)

    ## Test material serializer with short data
    def test_material_serializer_short_data(self):
        serializer = MaterialSerializer(data=self.short_material_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('size', serializer.errors)

    ## Test material serializer with long data
    def test_material_serializer_long_data(self):
        serializer = MaterialSerializer(data=self.long_material_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('size', serializer.errors)

    ## Test material serializer validation success
    def test_material_serializer_validation_success(self):
        serializer = MaterialSerializer(data=self.material_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('name', serializer.validated_data)
        self.assertIn('size', serializer.validated_data)
        self.assertIn('supplier', serializer.validated_data)

    ## Test material purchase serializer with empty data
    def test_material_purchase_serializer_empty_data(self):
        serializer = MaterialPurchaseSerializer(data=self.empty_material_purchase_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('material', serializer.errors)
        self.assertIn('supplier_address', serializer.errors)
        self.assertIn('purchase_quantity', serializer.errors)
        self.assertIn('purchase_cost', serializer.errors)
        self.assertIn('purchase_date', serializer.errors)

    ## Test material purchase serializer validation success
    def test_material_purchase_serializer_validation_success(self):
        serializer = MaterialPurchaseSerializer(data=self.material_purchase_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('material', serializer.validated_data)
        self.assertIn('supplier_address', serializer.validated_data)
        self.assertIn('purchase_quantity', serializer.validated_data)
        self.assertIn('purchase_cost', serializer.validated_data)
        self.assertIn('purchase_date', serializer.validated_data)

class TestMaterialView(APITestCase):
    pass

class TestMaterialPurchaseView(APITestCase):
    pass
