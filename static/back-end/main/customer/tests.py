from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from customer.serializers import CustomerSerializer
from customer.models import Customer
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for customer model
class TestCustomerModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901')

    ## Test string method for customer model
    def test_customer_string(self):
        self.assertEqual(str(self.customer), f'{self.customer.first_name} {self.customer.last_name}')

# Tests for customer serializer
class TestCustomerSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.long_string = 'a' * 256
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901')
        cls.empty_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone': '',
        }
        cls.short_data = {
            'first_name': 'J',
            'last_name': 'D',
            'email': 'j@e.com',
            'phone': '183043',
        }
        cls.long_data = {
            'first_name': cls.long_string,
            'last_name': cls.long_string,
            'email': cls.long_string + '@example.com',
            'phone': cls.long_string,
        }
        cls.create_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'phone': '1 (586) 375-3896',
        }
        cls.update_data = {
            'first_name': 'Bill',
            'last_name': 'Johnson',
            'email': 'billjohnson@example.com',
            'phone': '45 (192) 937-9329',
        }

    ## Test validate with empty data
    def test_validate_empty_data(self):
        serializer = CustomerSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors)
        self.assertIn('last_name', serializer.errors)
        self.assertIn('email', serializer.errors)
        self.assertIn('phone', serializer.errors)

    ## Test validate with data too long
    def test_validate_long_data(self):
        serializer = CustomerSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors)
        self.assertIn('last_name', serializer.errors)
        self.assertIn('email', serializer.errors)
        self.assertIn('phone', serializer.errors)

    ## Test validate with data too short
    def test_validate_short_data(self):
        serializer = CustomerSerializer(data=self.short_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors)
        self.assertIn('last_name', serializer.errors)
        self.assertIn('email', serializer.errors)
        self.assertIn('phone', serializer.errors)

    ## Test validate with incorrectly formatted phone number
    def test_validate_incorrectly_formatted_phone(self):
        self.create_data['phone'] = '+51-234-567-8901'
        serializer = CustomerSerializer(data=self.create_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('phone', serializer.errors)

    ## Test create success
    def test_create_success(self):
        serializer = CustomerSerializer(data=self.create_data)
        self.assertTrue(serializer.is_valid())
        customer: Customer = serializer.save()
        customer.refresh_from_db()
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(customer.first_name, self.create_data['first_name'])
        self.assertEqual(customer.last_name, self.create_data['last_name'])
        self.assertEqual(customer.email, self.create_data['email'])
        self.assertEqual(customer.phone, self.create_data['phone'])

    ## Test update success
    def test_update_success(self):
        serializer = CustomerSerializer(instance=self.customer, data=self.update_data)
        self.assertTrue(serializer.is_valid())
        customer: Customer = serializer.save()
        customer.refresh_from_db()
        self.assertEqual(customer.first_name, self.update_data['first_name'])
        self.assertEqual(customer.last_name, self.update_data['last_name'])
        self.assertEqual(customer.email, self.update_data['email'])
        self.assertEqual(customer.phone, self.update_data['phone'])

# Tests for customer view
class TestCustomerView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 'a' * 256
        cls.updated_email = 'kobe24@lakers.com'
        cls.list_url = reverse('customer-list')
        cls.detail_url = lambda pk: reverse('customer-detail', kwargs={'pk': pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901')
        cls.patch_data = {
            'email': cls.updated_email
        }
        cls.empty_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone': '',
        }
        cls.short_data = {
            'first_name': 'J',
            'last_name': 'D',
            'email': 'j@e.com',
            'phone': '183043',
        }
        cls.long_data = {
            'first_name': cls.long_string,
            'last_name': cls.long_string,
            'email': cls.long_string + '@example.com',
            'phone': cls.long_string,
        }
        cls.create_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'phone': '1 (586) 375-3896',
        }
        cls.update_data = {
            'first_name': 'Bill',
            'last_name': 'Johnson',
            'email': 'billjohnson@example.com',
            'phone': '45 (192) 937-9329',
        }

    ## Test get customer not found
    def test_get_customer_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(96))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Customer Not Found.')

    ## Test get customer success
    def test_get_customer_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.customer.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.customer.first_name)
        self.assertEqual(response.data['last_name'], self.customer.last_name)
        self.assertEqual(response.data['email'], self.customer.email)
        self.assertEqual(response.data['phone'], self.customer.phone)

    ## Test get customers success
    def test_get_customers_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Customer.objects.count())
        
    ## Test create customer with empty data
    def test_create_customer_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)
        
    ## Test create customer with short data
    def test_create_customer_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)
        
    ## Test create customer with long data
    def test_create_customer_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)

    ## Test create customer with existing email
    def test_create_customer_existing_email(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    ## Test create customer with invalid phone
    def test_create_customer_invalid_phone(self):
        self.client.force_authenticate(user=self.user)
        invalid_phone_data = self.create_data.copy()
        invalid_phone_data['phone'] = '+51-234-567-8901'
        response = self.client.post(self.list_url, data=invalid_phone_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.data)

    ## Test create customer success
    def test_create_customer_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        customer = Customer.objects.get(email=self.create_data['email'])
        self.assertEqual(customer.first_name, self.create_data['first_name'])
        self.assertEqual(customer.last_name, self.create_data['last_name'])
        self.assertEqual(customer.email, self.create_data['email'])
        self.assertEqual(customer.phone, self.create_data['phone'])

    ## Test update customer with empty data
    def test_update_customer_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url(self.customer.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)

    ## Test update customer with short data
    def test_update_customer_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url(self.customer.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)

    ## Test update customer with long data
    def test_update_customer_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url(self.customer.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)

    ## Test update customer with existing email
    def test_update_customer_existing_email(self):
        self.client.force_authenticate(user=self.user)
        another_customer = Customer.objects.create(first_name='Jane', last_name='Doe', email='janedoe@example.com', phone='1 (586) 375-3896')
        self.update_data['email'] = another_customer.email
        response = self.client.put(self.detail_url(self.customer.pk), data=self.update_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    ## Test update customer with invalid phone
    def test_update_customer_invalid_phone(self):
        self.client.force_authenticate(user=self.user)
        invalid_phone_data = self.update_data.copy()
        invalid_phone_data['phone'] = '+51-234-567-8901'
        response = self.client.put(self.detail_url(self.customer.pk), data=invalid_phone_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.data)

    ## Test update customer success
    def test_update_customer_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url(self.customer.pk), data=self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customer = Customer.objects.get(pk=self.customer.pk)
        self.assertEqual(customer.first_name, self.update_data['first_name'])
        self.assertEqual(customer.last_name, self.update_data['last_name'])
        self.assertEqual(customer.email, self.update_data['email'])
        self.assertEqual(customer.phone, self.update_data['phone'])

    ## Test partial update customer with empty data
    def test_partial_update_customer_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.customer.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)

    ## Test partial update customer with short data
    def test_partial_update_customer_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.customer.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)

    ## Test partial update customer with long data
    def test_partial_update_customer_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.customer.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)

    ## Test partial update customer with existing email
    def test_partial_update_customer_existing_email(self):
        self.client.force_authenticate(user=self.user)
        another_customer = Customer.objects.create(first_name='Jane', last_name='Doe', email='janedoe@example.com', phone='1 (586) 375-3896')
        response = self.client.patch(self.detail_url(self.customer.pk), data={'email': another_customer.email})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        
    ## Test partial update customer with invalid phone
    def test_partial_update_customer_with_invalid_phone(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.customer.pk), data={'phone': '+51-234-567-8901'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.data)

    ## Test partial update customer success
    def test_partial_update_customer_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.customer.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customer = Customer.objects.get(pk=self.customer.pk)
        self.assertEqual(customer.email, self.patch_data['email'])

    ## Test delete customer success
    def test_delete_customer_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.customer.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)
    