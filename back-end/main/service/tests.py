from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from service.serializers import ServiceSerializer
from service.models import Service
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for service model
class TestServiceModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.service = Service.objects.create(name='Test')

    ## Test string method for service model
    def test_service_string(self):
        self.assertEqual(str(self.service), self.service.name)

# Tests for service serializer
class TestServiceSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.long_string = 'a' * 501
        cls.service = Service.objects.create(name='Test', description='test service type')
        cls.empty_data = {'name': ''}
        cls.short_data = {'name': 'a'}
        cls.long_data = {'name': cls.long_string, 'description': cls.long_string}
        cls.create_data = {'name': 'name'}
        cls.update_data = {'name': 'updated', 'description': 'updated'}

    ## Test validate with empty data
    def test_validate_empty_data(self):
        serializer = ServiceSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test validate with short data
    def test_validate_short_data(self):
        serializer = ServiceSerializer(data=self.short_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test validate with long data
    def test_validate_long_data(self):
        serializer = ServiceSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('description', serializer.errors)

    ## Test validate with existing name
    def test_validate_existing_name(self):
        self.create_data['name'] = self.service.name
        serializer = ServiceSerializer(data=self.create_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test create success
    def test_create_success(self):
        serializer = ServiceSerializer(data=self.create_data)
        self.assertTrue(serializer.is_valid())

    ## Test update success
    def test_update_success(self):
        serializer = ServiceSerializer(instance= self.service, data=self.create_data)
        self.assertTrue(serializer.is_valid())

# Tests for service view
class TestServiceView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 'a' * 501
        cls.service = Service.objects.create(name='Test', description='test service type')
        cls.empty_data = {'name': ''}
        cls.short_data = {'name': 'a'}
        cls.long_data = {'name': cls.long_string, 'description': cls.long_string}
        cls.create_data = {'name': 'name', 'description': 'test'}
        cls.update_data = {'name': 'updated', 'description': 'updated'}
        cls.patch_data = {'description': 'test service description.'}
        cls.list_url = reverse('service-list')
        cls.detail_url = lambda pk: reverse('service-detail', kwargs={'pk': pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get service not found
    def test_get_service_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(96))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Service Not Found.')

    ## Test get service success
    def test_get_service_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.service.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.service.name)
        self.assertEqual(response.data['description'], self.service.description)

    ## Test get services success
    def test_get_services_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Service.objects.count())

    ## Test create service with empty data
    def test_create_service_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test create service with short data
    def test_create_service_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test create service with long data
    def test_create_service_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('description', response.data)

    ## Test create service with existing name
    def test_create_service_existing_name(self):
        self.client.force_authenticate(user=self.user)
        self.create_data['name'] = self.service.name
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test create service success
    def test_create_service_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.count(), 2)
        service = Service.objects.get(name=self.create_data['name'])
        self.assertEqual(service.name, self.create_data['name'])
        self.assertEqual(service.description, self.create_data['description'])

    ## Test update service with empty data
    def test_update_service_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.service.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test update service with short data
    def test_update_service_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.service.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test update service with long data
    def test_update_service_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.service.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test update service success
    def test_update_service_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.service.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        service = Service.objects.get(pk=self.service.pk)
        self.assertEqual(service.description, self.patch_data['description'])

    ## Test delete service success
    def test_delete_service_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.service.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Service.objects.count(), 0)
