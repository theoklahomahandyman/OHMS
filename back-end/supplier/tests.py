from supplier.serializers import SupplierSerializer, SupplierAddressSerializer
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from supplier.models import Supplier, SupplierAddress
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

''' Tests for supplier models '''
class TestSupplierModels(TestCase):

    ''' Set up test data '''
    @classmethod
    def setUpTestData(cls):
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)

    ''' Clean up test data '''
    @classmethod
    def tearDownClass(cls):
        cls.address.delete()
        cls.supplier.delete()

    ''' Test string method for supplier model '''
    def test_supplier_string(self):
        self.assertEqual(str(self.supplier), self.supplier.name)

    ''' Test string method for supplier address model '''
    def test_supplier_address_string(self):
        self.assertEqual(str(self.address), f'{self.address.street_address} {self.address.city}, {self.address.state} {self.address.zip}')

''' Tests for supplier serializers '''
class TestSupplierSerializers(TestCase):

    ''' Set up test data '''
    @classmethod
    def setUpTestData(cls):
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)
        cls.long_string = 'a' * 501
        cls.empty_supplier_address_data = {'street_address': '', 'city': '', 'state': '', 'zip': ''}
        cls.short_supplier_address_data = {'street_address': 'T', 'city': 'C', 'state': 'O', 'zip': 482}
        cls.long_supplier_address_data = {'street_address': cls.long_string, 'city': cls.long_string, 'state': cls.long_string, 'zip': 57390238573}
        cls.supplier_address_data = {'street_address': '164 Main St', 'city': 'City', 'state': 'State', 'zip': 48023}
        cls.empty_supplier_data = {'name': '', 'notes': '', 'addresses': [cls.empty_supplier_address_data]}
        cls.short_supplier_data = {'name': 'T', 'notes': '', 'addresses': [cls.short_supplier_address_data]}
        cls.long_supplier_data = {'name': cls.long_string, 'notes': cls.long_string, 'addresses': [cls.long_supplier_address_data]}
        cls.supplier_data = {'name': 'test', 'notes': 'test notes', 'addresses': [cls.supplier_address_data]}
        cls.supplier_with_address = {'name': 'supplier with address', 'notes': 'supplier with address', 'addresses': [{'street_address': '123 Main St', 'city': 'Test', 'state': 'Test', 'zip': 28342, 'notes': 'test address'}]}

    ''' Clean up test data '''
    @classmethod
    def tearDownClass(cls):
        cls.address.delete()
        cls.supplier.delete()

    ''' Test supplier serializer with empty data '''
    def test_supplier_serializer_empty_data(self):
        serializer = SupplierSerializer(data=self.empty_supplier_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ''' Test supplier serializer with short data '''
    def test_supplier_serializer_short_data(self):
        serializer = SupplierSerializer(data=self.short_supplier_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ''' Test supplier serializer with long data '''
    def test_supplier_serializer_long_data(self):
        serializer = SupplierSerializer(data=self.long_supplier_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('notes', serializer.errors)

    ''' Test supplier serializer validation success '''
    def test_supplier_serializer_validation_success(self):
        serializer = SupplierSerializer(data=self.supplier_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('name', serializer.validated_data)
        self.assertIn('notes', serializer.validated_data)

    ''' Test supplier address serializer with empty data '''
    def test_supplier_address_serializer_empty_data(self):
        serializer = SupplierAddressSerializer(data=self.empty_supplier_address_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('street_address', serializer.errors)
        self.assertIn('city', serializer.errors)
        self.assertIn('state', serializer.errors)
        self.assertIn('zip', serializer.errors)

    ''' Test supplier address serializer with short data '''
    def test_supplier_address_serializer_short_data(self):
        serializer = SupplierAddressSerializer(data=self.short_supplier_address_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('street_address', serializer.errors)
        self.assertIn('city', serializer.errors)
        self.assertIn('state', serializer.errors)
        self.assertIn('zip', serializer.errors)

    ''' Test supplier address serializer with long data '''
    def test_supplier_address_serializer_long_data(self):
        serializer = SupplierAddressSerializer(data=self.long_supplier_address_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('street_address', serializer.errors)
        self.assertIn('city', serializer.errors)
        self.assertIn('state', serializer.errors)
        self.assertIn('zip', serializer.errors)

    ''' Test supplier address serializer validation success '''
    def test_supplier_address_serializer_validation_success(self):
        serializer = SupplierAddressSerializer(data=self.supplier_address_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('street_address', serializer.validated_data)
        self.assertIn('city', serializer.validated_data)
        self.assertIn('state', serializer.validated_data)
        self.assertIn('zip', serializer.validated_data)

    ''' Test supplier with address serializer validation success '''
    def test_supplier_with_address_serializer_validation_success(self):
        serializer = SupplierSerializer(data=self.supplier_with_address)
        self.assertTrue(serializer.is_valid())
        supplier_with_address = serializer.save()
        self.assertIn('name', supplier_with_address)
        self.assertIn('notes', supplier_with_address)
        self.assertIn('addresses', supplier_with_address)

''' Tests for supplier view '''
class TestSupplierView(APITestCase):

    ''' Set up test data '''
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 'a' * 501
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.long_string = 'a' * 501
        cls.empty_data = {'name': ''}
        cls.short_data = {'name': 'T'}
        cls.long_data = {'name': cls.long_string, 'notes': cls.long_string}
        cls.create_data = {'name': 'test brand new supplier name', 'notes': 'test notes'}
        cls.update_data = {'name': 'updated', 'notes': 'updated notes'}
        cls.patch_data = {'notes': 'test service description.'}
        cls.list_url = reverse('supplier-list')
        cls.detail_url = lambda pk: reverse('supplier-detail', kwargs={'pk': pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ''' Test get supplier not found '''
    def test_get_supplier_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(96))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Supplier Not Found.')

    ''' Test get supplier success '''
    def test_get_supplier_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.supplier.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.supplier.name)
        self.assertEqual(response.data['notes'], self.supplier.notes)

    ''' Test get suppliers success '''
    def test_get_suppliers_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Supplier.objects.count())

    ''' Test create supplier with empty data '''
    def test_create_supplier_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ''' Test create supplier with short data '''
    def test_create_supplier_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ''' Test create supplier with long data '''
    def test_create_supplier_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('notes', response.data)

    ''' Test create supplier with existing name '''
    def test_create_supplier_existing_name(self):
        self.client.force_authenticate(user=self.user)
        self.create_data['name'] = self.supplier.name
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ''' Test create supplier success '''
    def test_create_supplier_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 2)
        supplier = Supplier.objects.get(name=self.create_data['name'])
        self.assertEqual(supplier.name, self.create_data['name'])
        self.assertEqual(supplier.notes, self.create_data['notes'])

    ''' Test update supplier with empty data '''
    def test_update_supplier_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.supplier.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ''' Test update supplier with short data '''
    def test_update_supplier_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.supplier.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ''' Test update supplier with long data '''
    def test_update_supplier_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.supplier.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('notes', response.data)

    ''' Test update supplier success '''
    def test_update_supplier_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.supplier.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        supplier = Supplier.objects.get(pk=self.supplier.pk)
        self.assertEqual(supplier.notes, self.patch_data['notes'])

    ''' Test delete supplier success '''
    def test_delete_supplier_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.supplier.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Supplier.objects.count(), 0)
