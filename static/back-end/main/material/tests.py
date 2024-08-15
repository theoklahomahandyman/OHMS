from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from supplier.models import Supplier, SupplierAddress
from material.serializers import MaterialSerializer
from material.models import Material
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for material models
class TestMaterialModels(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.material = Material.objects.create(name='material', size='2 inch X 4 inch X 8 feet')

    ## Test string method for material model
    def test_material_string(self):
        self.assertEqual(str(self.material), f'OHMS{self.material.pk}-MAT')

class TestMaterialSerializers(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.material = Material.objects.create(name='material', size='2 inch X 4 inch X 8 feet')
        cls.long_string = 'a' * 501
        cls.empty_material_data = {'name': '', 'size': ''}
        cls.short_material_data = {'name': 'T', 'size': 'S'}
        cls.long_material_data = {'name': cls.long_string, 'size': cls.long_string}
        cls.material_data = {'name': 'material test', 'size': 'material size'}

    ## Test material serializer with empty data
    def test_material_serializer_empty_data(self):
        serializer = MaterialSerializer(data=self.empty_material_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('size', serializer.errors)

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

class TestMaterialView(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 'a' * 501
        cls.long_string = 'a' * 501
        cls.empty_data = {'name': '', 'size': ''}
        cls.short_data = {'name': 'T', 'size': 'S'}
        cls.long_data = {'name': cls.long_string, 'size': cls.long_string}
        cls.create_data = {'name': 'material test', 'size': 'material size'}
        cls.update_data = {'name': 'material test', 'size': 'material size'}
        cls.patch_data = {'notes': 'test service description.'}
        cls.list_url = reverse('supplier-list')
        cls.detail_url = lambda pk: reverse('supplier-detail', kwargs={'pk': pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))
    
