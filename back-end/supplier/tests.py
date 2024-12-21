from supplier.serializers import SupplierSerializer, SupplierAddressSerializer
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from supplier.models import Supplier, SupplierAddress
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for supplier models
class TestSupplierModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)

    ## Test string method for supplier model
    def test_supplier_string(self):
        self.assertEqual(str(self.supplier), self.supplier.name)

    ## Test string method for supplier address model
    def test_supplier_address_string(self):
        self.assertEqual(str(self.address), f'{self.address.street_address} {self.address.city}, {self.address.state} {self.address.zip}')

# Tests for supplier serializers
class TestSupplierSerializers(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)
        cls.long_string = 'a' * 501
        cls.empty_supplier_data = {'name': ''}
        cls.short_supplier_data = {'name': 'T'}
        cls.long_supplier_data = {'name': cls.long_string, 'notes': cls.long_string}
        cls.supplier_data = {'name': 'test', 'notes': 'test notes'}
        cls.empty_supplier_address_data = {'supplier': '', 'street_address': '', 'city': '', 'state': '', 'zip': ''}
        cls.short_supplier_address_data = {'supplier': cls.supplier.pk, 'street_address': 'T', 'city': 'C', 'state': 'O', 'zip': 482}
        cls.long_supplier_address_data = {'supplier': cls.supplier.pk, 'street_address': cls.long_string, 'city': cls.long_string, 'state': cls.long_string, 'zip': 57390238573}
        cls.supplier_address_data = {'supplier': cls.supplier.pk, 'street_address': '164 Main St', 'city': 'City', 'state': 'State', 'zip': 48023}

    ## Test supplier serializer with empty data
    def test_supplier_serializer_empty_data(self):
        serializer = SupplierSerializer(data=self.empty_supplier_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test supplier serializer with short data
    def test_supplier_serializer_short_data(self):
        serializer = SupplierSerializer(data=self.short_supplier_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test supplier serializer with long data
    def test_supplier_serializer_long_data(self):
        serializer = SupplierSerializer(data=self.long_supplier_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('notes', serializer.errors)

    ## Test supplier serializer validation success
    def test_supplier_serializer_validation_success(self):
        serializer = SupplierSerializer(data=self.supplier_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('name', serializer.validated_data)
        self.assertIn('notes', serializer.validated_data)

    ## Test supplier address serializer with empty data
    def test_supplier_address_serializer_empty_data(self):
        serializer = SupplierAddressSerializer(data=self.empty_supplier_address_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('supplier', serializer.errors)
        self.assertIn('street_address', serializer.errors)
        self.assertIn('city', serializer.errors)
        self.assertIn('state', serializer.errors)
        self.assertIn('zip', serializer.errors)

    ## Test supplier address serializer with short data
    def test_supplier_address_serializer_short_data(self):
        serializer = SupplierAddressSerializer(data=self.short_supplier_address_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('street_address', serializer.errors)
        self.assertIn('city', serializer.errors)
        self.assertIn('state', serializer.errors)
        self.assertIn('zip', serializer.errors)

    ## Test supplier address serializer with long data
    def test_supplier_address_serializer_long_data(self):
        serializer = SupplierAddressSerializer(data=self.long_supplier_address_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('street_address', serializer.errors)
        self.assertIn('city', serializer.errors)
        self.assertIn('state', serializer.errors)
        self.assertIn('zip', serializer.errors)

    ## Test supplier address serializer validation success
    def test_supplier_address_serializer_validation_success(self):
        serializer = SupplierAddressSerializer(data=self.supplier_address_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('supplier', serializer.validated_data)
        self.assertIn('street_address', serializer.validated_data)
        self.assertIn('city', serializer.validated_data)
        self.assertIn('state', serializer.validated_data)
        self.assertIn('zip', serializer.validated_data)

# Tests for supplier view
class TestSupplierView(APITestCase):

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
        cls.create_data = {'name': 'test', 'notes': 'test notes'}
        cls.update_data = {'name': 'updated', 'notes': 'updated notes'}
        cls.patch_data = {'notes': 'test service description.'}
        cls.list_url = reverse('supplier-list')
        cls.detail_url = lambda pk: reverse('supplier-detail', kwargs={'pk': pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get supplier not found
    def test_get_supplier_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(96))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Supplier Not Found.')

    ## Test get supplier success
    def test_get_supplier_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.supplier.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.supplier.name)
        self.assertEqual(response.data['notes'], self.supplier.notes)

    ## Test get suppliers success
    def test_get_suppliers_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Supplier.objects.count())

    ## Test create supplier with empty data
    def test_create_supplier_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test create supplier with short data
    def test_create_supplier_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test create supplier with long data
    def test_create_supplier_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('notes', response.data)

    ## Test create supplier with existing name
    def test_create_supplier_existing_name(self):
        self.client.force_authenticate(user=self.user)
        self.create_data['name'] = self.supplier.name
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test create supplier success
    def test_create_supplier_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 2)
        supplier = Supplier.objects.get(name=self.create_data['name'])
        self.assertEqual(supplier.name, self.create_data['name'])
        self.assertEqual(supplier.notes, self.create_data['notes'])

    ## Test update supplier with empty data
    def test_update_supplier_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.supplier.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test update supplier with short data
    def test_update_supplier_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.supplier.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test update supplier with long data
    def test_update_supplier_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.supplier.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('notes', response.data)

    ## Test update supplier success
    def test_update_supplier_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.supplier.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        supplier = Supplier.objects.get(pk=self.supplier.pk)
        self.assertEqual(supplier.notes, self.patch_data['notes'])

    ## Test delete supplier success
    def test_delete_supplier_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.supplier.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Supplier.objects.count(), 0)

# Tests for supplier address view
class TestSupplierAddressView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 'a' * 501
        cls.supplier = Supplier.objects.create(name='test')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)
        cls.long_string = 'a' * 501
        cls.empty_data = {'street_address': '', 'city': '', 'state': '', 'zip': ''}
        cls.short_data = {'street_address': 'T', 'city': 'C', 'state': 'O', 'zip': 482}
        cls.long_data = {'street_address': cls.long_string, 'city': cls.long_string, 'state': cls.long_string, 'zip': 57390238573, 'notes': cls.long_string}
        cls.create_data = {'street_address': '164 Main St', 'city': 'City', 'state': 'State', 'zip': 48023, 'notes': 'notes'}
        cls.update_data = {'street_address': '749 Fairview St', 'city': 'A-Town', 'state': 'ST', 'zip': 52023, 'notes': 'updated notes'}
        cls.patch_data = {'notes': 'test service description.'}
        cls.list_url = lambda supplier_pk: reverse('supplier-address-list', kwargs={'supplier_pk': supplier_pk})
        cls.detail_url = lambda supplier_pk, address_pk: reverse('supplier-address-detail', kwargs={'supplier_pk': supplier_pk, 'address_pk': address_pk})
        cls.representation_url = lambda address_pk: reverse('supplier-address', kwargs={'pk': address_pk})
        cls.representation = f'{cls.address.street_address} {cls.address.city}, {cls.address.state} {cls.address.zip}'
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get supplier address not found
    def test_get_supplier_address_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.supplier.pk, 79027269))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Supplier Address Not Found.')

    ## Test get supplier address success
    def test_get_supplier_address_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.supplier.pk, self.address.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['street_address'], self.address.street_address)
        self.assertEqual(response.data['city'], self.address.city)
        self.assertEqual(response.data['state'], self.address.state)
        self.assertEqual(response.data['zip'], self.address.zip)
        self.assertEqual(response.data['notes'], self.address.notes)

    ## Test get supplier addresses success
    def test_get_supplier_addresses_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url(self.supplier.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), SupplierAddress.objects.filter(supplier=self.supplier).count())

    ## Test create supplier address with empty data
    def test_create_supplier_address_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.supplier.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('street_address', response.data)
        self.assertIn('city', response.data)
        self.assertIn('state', response.data)
        self.assertIn('zip', response.data)

    ## Test create supplier address with short data
    def test_create_supplier_address_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.supplier.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('street_address', response.data)
        self.assertIn('city', response.data)
        self.assertIn('state', response.data)
        self.assertIn('zip', response.data)

    ## Test create supplier address with long data
    def test_create_supplier_address_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.supplier.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('street_address', response.data)
        self.assertIn('city', response.data)
        self.assertIn('state', response.data)
        self.assertIn('zip', response.data)
        self.assertIn('notes', response.data)

    ## Test create supplier address success
    def test_create_supplier_address_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.supplier.pk), data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SupplierAddress.objects.count(), 2)
        address = SupplierAddress.objects.get(street_address=self.create_data['street_address'])
        self.assertEqual(address.street_address, self.create_data['street_address'])
        self.assertEqual(address.city, self.create_data['city'])
        self.assertEqual(address.state, self.create_data['state'])
        self.assertEqual(address.zip, self.create_data['zip'])
        self.assertEqual(address.notes, self.create_data['notes'])

    ## Test update supplier address with empty data
    def test_update_supplier_address_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.supplier.pk, self.address.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('street_address', response.data)
        self.assertIn('city', response.data)
        self.assertIn('state', response.data)
        self.assertIn('zip', response.data)

    ## Test update supplier address with short data
    def test_update_supplier_address_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.supplier.pk, self.address.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('street_address', response.data)
        self.assertIn('city', response.data)
        self.assertIn('state', response.data)
        self.assertIn('zip', response.data)

    ## Test update supplier address with long data
    def test_update_supplier_address_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.supplier.pk, self.address.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('street_address', response.data)
        self.assertIn('city', response.data)
        self.assertIn('state', response.data)
        self.assertIn('zip', response.data)
        self.assertIn('notes', response.data)

    ## Test update supplier address success
    def test_update_supplier_address_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.supplier.pk, self.address.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        address = SupplierAddress.objects.get(pk=self.address.pk)
        self.assertEqual(address.notes, self.patch_data['notes'])

    ## Test delete supplier address success
    def test_delete_supplier_address_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.supplier.pk, self.address.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SupplierAddress.objects.count(), 0)

    ## Test get supplier address representation success
    def test_get_supplier_address_representation_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.representation_url(self.address.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['representation'], self.representation)
