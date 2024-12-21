from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from material.serializers import MaterialSerializer
from material.models import Material
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for material serializer
class TestMaterialSerializers(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.material = Material.objects.create(name='material', size='2 inch X 4 inch X 8 feet')
        cls.long_string = 'a' * 501
        cls.empty_data = {'name': '', 'size': ''}
        cls.short_data = {'name': 'T', 'size': 'S'}
        cls.long_data = {'name': cls.long_string, 'size': cls.long_string}
        cls.valid_data = {'name': 'material test', 'size': 'material size'}

    ## Test material serializer with empty data
    def test_material_serializer_empty_data(self):
        serializer = MaterialSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('size', serializer.errors)

    ## Test material serializer with short data
    def test_material_serializer_short_data(self):
        serializer = MaterialSerializer(data=self.short_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('size', serializer.errors)

    ## Test material serializer with long data
    def test_material_serializer_long_data(self):
        serializer = MaterialSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('size', serializer.errors)

    ## Test material serializer validation success
    def test_material_serializer_validation_success(self):
        serializer = MaterialSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('name', serializer.validated_data)
        self.assertIn('size', serializer.validated_data)

class TestMaterialView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 'a' * 501
        cls.empty_data = {'name': '', 'size': ''}
        cls.short_data = {'name': 'T', 'size': 'S'}
        cls.long_data = {'name': cls.long_string, 'size': cls.long_string, 'description': cls.long_string}
        cls.create_data = {'name': 'material test', 'size': 'material size', 'description': 'material description'}
        cls.patch_data = {'name': 'an updated name'}
        cls.list_url = reverse('material-list')
        cls.detail_url = lambda pk: reverse('material-detail', kwargs={'pk': pk})
        cls.material = Material.objects.create(name='material', size='2 inch X 4 inch X 8 feet', description='description')
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get material not found
    def test_get_material_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(96))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Material Not Found.')

    ## Test get material success
    def test_get_material_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.material.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.material.name)
        self.assertEqual(response.data['size'], self.material.size)
        self.assertEqual(response.data['description'], self.material.description)
        self.assertEqual(response.data['available_quantity'], self.material.available_quantity)
        self.assertEqual(float(response.data['unit_cost']), self.material.unit_cost)

    ## Test get materials success
    def test_get_materials_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Material.objects.count())

    ## Test create material with empty data
    def test_create_material_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('size', response.data)

    ## Test create material with short data
    def test_create_material_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('size', response.data)

    ## Test create material with long data
    def test_create_material_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('size', response.data)
        self.assertIn('description', response.data)

    ## Test create material with existing name and size
    def test_create_material_existing_name_size(self):
        self.client.force_authenticate(user=self.user)
        self.create_data['name'] = self.material.name
        self.create_data['size'] = self.material.size
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    ## Test create material success
    def test_create_material_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Material.objects.count(), 2)
        material = Material.objects.get(name=self.create_data['name'], size=self.create_data['size'])
        self.assertEqual(material.name, self.create_data['name'])
        self.assertEqual(material.size, self.create_data['size'])
        self.assertEqual(material.description, self.create_data['description'])

    ## Test update material with empty data
    def test_update_material_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.material.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('size', response.data)

    ## Test update material with short data
    def test_update_material_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.material.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('size', response.data)

    ## Test update material with long data
    def test_update_material_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.material.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('size', response.data)
        self.assertIn('description', response.data)

    ## Test update material success
    def test_update_material_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.material.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        material = Material.objects.get(pk=self.material.pk)
        self.assertEqual(material.name, self.patch_data['name'])

    ## Test delete material success
    def test_delete_material_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.material.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Material.objects.count(), 0)
