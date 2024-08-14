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
        MaterialPurchase.objects.create(material=self.material, purchase_quantity=0, purchase_cost=0, purchase_date='2024-08-01')
        self.material.refresh_from_db()
        self.assertEqual(self.material.unit_cost, 0.0)
        self.assertEqual(self.material.available_quantity, 0)

    ## Test save method for material purchase model
    def test_material_purchase_save(self):
        material_purchase = MaterialPurchase.objects.create(material=self.material, purchase_quantity=3, purchase_cost=56.32, purchase_date='2024-08-01')
        self.material.refresh_from_db()
        expected_unit_cost = material_purchase.purchase_cost / material_purchase.purchase_quantity
        self.assertEqual(self.material.unit_cost, expected_unit_cost)
        self.assertEqual(self.material.available_quantity, material_purchase.purchase_quantity)

    ## Test string method for material purchase model
    def test_material_purchase_string(self):
        material_purchase = MaterialPurchase.objects.create(material=self.material, purchase_quantity=3, purchase_cost=56.32, purchase_date='2024-08-01')
        self.assertEqual(str(material_purchase), f'{self.material.name} - {material_purchase.purchase_quantity} units purchased')
