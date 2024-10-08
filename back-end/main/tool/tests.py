from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from tool.serializers import ToolSerializer
from tool.models import Tool
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for tool serializer
class TestToolSerializers(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.long_string = 'a' * 501
        cls.empty_data = {'name': '', 'description': '', 'unit_cost': '', 'available_quantity': ''}
        cls.short_data = {'name': 't', 'description': 'd', 'unit_cost': 5.30, 'available_quantity': 8}
        cls.long_data = {'name': cls.long_string, 'description': cls.long_string, 'unit_cost': 546546845646846818616548645616848618615.30, 'available_quantity': 8}
        cls.valid_data = {'name': 'name', 'description': 'description', 'unit_cost': 5.30, 'available_quantity': 8}

    ## Test tool serializer with empty data
    def test_tool_serializer_empty_data(self):
        serializer = ToolSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test tool serializer with short data
    def test_tool_serializer_short_data(self):
        serializer = ToolSerializer(data=self.short_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test tool serializer with long data
    def test_tool_serializer_long_data(self):
        serializer = ToolSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('description', serializer.errors)
        self.assertIn('unit_cost', serializer.errors)

    ## Test tool serializer validation success
    def test_tool_serializer_validation_success(self):
        serializer = ToolSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('name', serializer.validated_data)
        self.assertIn('description', serializer.validated_data)
        self.assertIn('unit_cost', serializer.validated_data)
        self.assertIn('available_quantity', serializer.validated_data)


class TestToolView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 'a' * 501
        cls.empty_data = {'name': '', 'description': '', 'unit_cost': '', 'available_quantity': ''}
        cls.short_data = {'name': 't', 'description': 'd', 'unit_cost': 5.30, 'available_quantity': 8}
        cls.long_data = {'name': cls.long_string, 'description': cls.long_string, 'unit_cost': 546546845646846818616548645616848618615.30, 'available_quantity': 8}
        cls.create_data = {'name': 'name', 'description': 'description', 'unit_cost': 5.30, 'available_quantity': 8}
        cls.patch_data = {'name': 'updated name'}
        cls.list_url = reverse('tool-list')
        cls.detail_url = lambda pk: reverse('tool-detail', kwargs={'pk': pk})
        cls.tool = Tool.objects.create(name='tool', description='description', unit_cost=7.54, available_quantity=15)
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get tool not found
    def test_get_tool_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(96))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Tool Not Found.')

    ## Test get tool success
    def test_get_tool_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.tool.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.tool.name)
        self.assertEqual(response.data['description'], self.tool.description)
        self.assertEqual(response.data['available_quantity'], self.tool.available_quantity)
        self.assertEqual(float(response.data['unit_cost']), self.tool.unit_cost)

    ## Test get tools success
    def test_get_tools_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Tool.objects.count())

    ## Test create tool with empty data
    def test_create_tool_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test create tool with short data
    def test_create_tool_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test create tool with long data
    def test_create_tool_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('description', response.data)
        self.assertIn('unit_cost', response.data)

    ## Test create tool success
    def test_create_tool_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tool.objects.count(), 2)
        tool = Tool.objects.get(name=self.create_data['name'])
        self.assertEqual(tool.name, self.create_data['name'])
        self.assertEqual(tool.description, self.create_data['description'])
        self.assertEqual(float(tool.unit_cost), self.create_data['unit_cost'])
        self.assertEqual(tool.available_quantity, self.create_data['available_quantity'])

    ## Test update tool with empty data
    def test_update_tool_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.tool.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test update tool with short data
    def test_update_tool_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.tool.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test update tool with long data
    def test_update_tool_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.tool.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('description', response.data)
        self.assertIn('unit_cost', response.data)

    ## Test update tool success
    def test_update_tool_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.tool.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tool = Tool.objects.get(pk=self.tool.pk)
        self.assertEqual(tool.name, self.patch_data['name'])

    ## Test delete tool success
    def test_delete_tool_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.tool.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tool.objects.count(), 0)
