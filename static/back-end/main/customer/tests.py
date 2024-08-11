from rest_framework.test import APITestCase, APIClient
from customer.models import Customer
from rest_framework import status
from django.test import TestCase
from django.urls import reverse

# Tests for customer model
class TestCustomerModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901')

    ## Test string method for user model
    def test_user_string(self):
        self.assertEqual(str(self.customer), f'{self.customer.first_name} {self.customer.last_name}')
