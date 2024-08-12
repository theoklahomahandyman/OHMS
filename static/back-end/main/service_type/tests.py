from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
# from service_type.serializers import ServiceTypeSerializer
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
        