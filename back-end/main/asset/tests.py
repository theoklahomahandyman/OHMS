from asset.serializers import AssetSerializer, AssetMaintenanceSerializer
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from asset.models import Asset, AssetMaintenance
from django.utils import timezone
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for asset models
class TestAssetModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.asset = Asset.objects.create(name='asset', serial_number='12942034', description='asset description', unit_cost=12.30, rental_cost=14.25, last_maintenance=timezone.now().date() - timezone.timedelta(weeks=6), next_maintenance=timezone.now().date() + timezone.timedelta(weeks=20), usage=500, location='location', condition=Asset.CONDITION_CHOICES.GOOD, status=Asset.STATUS_CHOICES.AVAILABLE, notes='asset notes')
        cls.maintenance_data = {'asset': cls.asset, 'date': timezone.now().date(), 'condition': None, 'status': None, 'next_maintenance': None, 'notes': 'missing fields test', 'current_usage': 0 }

    def test_asset_default_last_maintenance(self):
        date = Asset.default_last_maintenance()
        expected_date = timezone.now().date()
        self.assertEqual(date, expected_date)

    def test_asset_default_next_maintenance(self):
        date = Asset.default_next_maintenance()
        expected_date = timezone.now().date() +  timezone.timedelta(weeks=26)
        self.assertEqual(date, expected_date)

    def test_asset_maintenance_save(self):
        maintenance = AssetMaintenance.objects.create(**self.maintenance_data)
        self.assertEqual(maintenance.asset.next_maintenance, maintenance.date + timezone.timedelta(weeks=26))
        self.assertEqual(maintenance.asset.condition, Asset.CONDITION_CHOICES.GOOD)
        self.assertEqual(maintenance.asset.status, Asset.STATUS_CHOICES.AVAILABLE)
        self.assertEqual(maintenance.asset.usage, maintenance.current_usage)

# Tests for asset serializer
class TestAssetSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.long_string = 't' * 501
        cls.empty_data = {'name': '', 'serial_number': '', 'description': '', 'unit_cost': '', 'rental_cost': '', 'last_maintenance': '', 'next_maintenance': '', 'usage': '', 'location': '', 'condition': '', 'status': '', 'notes': ''}
        cls.short_data = {'name': 't', 'serial_number': '1', 'description': 'test', 'unit_cost': 0.0, 'rental_cost': 0.0, 'last_maintenance': None, 'next_maintenance': None, 'usage': 0.0, 'location': 'test', 'condition': 'good', 'status': 'available', 'notes': 'test'}
        cls.long_data = {'name': cls.long_string, 'serial_number': cls.long_string, 'description': cls.long_string, 'unit_cost': 0.0, 'rental_cost': 0.0, 'last_maintenance': None, 'next_maintenance': None, 'usage': 0.0, 'location': cls.long_string, 'condition': cls.long_string, 'status': cls.long_string, 'notes': cls.long_string}
        cls.negative_data = {'name': 'name', 'serial_number': '1', 'description': 'test', 'unit_cost': -5.65, 'rental_cost': -8.62, 'last_maintenance': None, 'next_maintenance': None, 'usage': -94.14, 'location': 'location', 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.IN_USE, 'notes': 'test'}
        cls.invalid_date_data = {'name': 'name', 'serial_number': '1', 'description': 'test', 'unit_cost': 5.65, 'rental_cost': 8.62, 'last_maintenance': timezone.now().date(), 'next_maintenance': timezone.now().date() - timezone.timedelta(weeks=26), 'usage': 94.14, 'location': 'location', 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.IN_USE, 'notes': 'test'}
        cls.valid_data = {'name': 'name', 'serial_number': '1', 'description': 'test', 'unit_cost': 5.65, 'rental_cost': 8.62, 'last_maintenance': timezone.now().date(), 'next_maintenance': timezone.now().date() + timezone.timedelta(weeks=26), 'usage': 94.14, 'location': 'location', 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.IN_USE, 'notes': 'test'}

    ## Test asset serializer with empty data
    def test_asset_serializer_empty_data(self):
        serializer = AssetSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('serial_number', serializer.errors)
        self.assertIn('unit_cost', serializer.errors)
        self.assertIn('rental_cost', serializer.errors)
        self.assertIn('last_maintenance', serializer.errors)
        self.assertIn('next_maintenance', serializer.errors)
        self.assertIn('usage', serializer.errors)
        self.assertIn('condition', serializer.errors)
        self.assertIn('status', serializer.errors)

    ## Test asset serializer with short data
    def test_asset_serializer_short_data(self):
        serializer = AssetSerializer(data=self.short_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test asset serializer with long data
    def test_asset_serializer_long_data(self):
        serializer = AssetSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('serial_number', serializer.errors)
        self.assertIn('description', serializer.errors)
        self.assertIn('location', serializer.errors)
        self.assertIn('condition', serializer.errors)
        self.assertIn('status', serializer.errors)
        self.assertIn('notes', serializer.errors)

    ## Test asset serializer with negative data
    def test_asset_serializer_negative_data(self):
        serializer = AssetSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('unit_cost', serializer.errors)
        self.assertIn('rental_cost', serializer.errors)
        self.assertIn('usage', serializer.errors)

    ## Test asset serializer with invalid date data
    def test_asset_serializer_invalid_date_data(self):
        serializer = AssetSerializer(data=self.invalid_date_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('next_maintenance', serializer.errors)

    ## Test asset serializer with valid data
    def test_asset_serializer_valid_data(self):
        serializer = AssetSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('name', serializer.validated_data)
        self.assertIn('serial_number', serializer.validated_data)
        self.assertIn('description', serializer.validated_data)
        self.assertIn('unit_cost', serializer.validated_data)
        self.assertIn('rental_cost', serializer.validated_data)
        self.assertIn('last_maintenance', serializer.validated_data)
        self.assertIn('next_maintenance', serializer.validated_data)
        self.assertIn('usage', serializer.validated_data)
        self.assertIn('location', serializer.validated_data)
        self.assertIn('condition', serializer.validated_data)
        self.assertIn('status', serializer.validated_data)
        self.assertIn('notes', serializer.validated_data)

# Tests for asset maintenance serializer
class TestAssetMaintenanceSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.long_string = 't' * 501
        cls.asset = Asset.objects.create(name='asset', serial_number='12942034', description='asset description', unit_cost=12.30, rental_cost=14.25, last_maintenance=timezone.now().date() - timezone.timedelta(weeks=6), next_maintenance=timezone.now().date() + timezone.timedelta(weeks=20), usage=500, location='location', condition=Asset.CONDITION_CHOICES.GOOD, status=Asset.STATUS_CHOICES.AVAILABLE, notes='asset notes')
        cls.maintenance = AssetMaintenance.objects.create(asset=cls.asset, date=timezone.now().date() - timezone.timedelta(weeks=6), next_maintenance=timezone.now().date() + timezone.timedelta(weeks=20), current_usage=500, condition=Asset.CONDITION_CHOICES.GOOD, status=Asset.STATUS_CHOICES.AVAILABLE, notes='maintenance event 1')
        cls.empty_data = {'asset': '', 'date': '', 'next_maintenance': '', 'current_usage': '', 'condition': '', 'status': '', 'notes': ''}
        cls.long_data = {'asset': cls.asset.pk, 'date': timezone.now().date() - timezone.timedelta(weeks=6), 'next_maintenance': timezone.now().date() + timezone.timedelta(weeks=20), 'current_usage': 6105156165165156156181156156165800, 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.AVAILABLE, 'notes': cls.long_string}
        cls.negative_data = {'asset': cls.asset.pk, 'date': timezone.now().date() - timezone.timedelta(weeks=32), 'next_maintenance': timezone.now().date() - timezone.timedelta(weeks=6), 'current_usage': -250, 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.AVAILABLE, 'notes': 'maintenance event 1'}
        cls.invalid_date_data = {'asset': cls.asset.pk, 'date': timezone.now().date() - timezone.timedelta(weeks=6), 'next_maintenance': timezone.now().date() - timezone.timedelta(weeks=20), 'current_usage': 250, 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.AVAILABLE, 'notes': 'maintenance event 1'}
        cls.valid_data = {'asset': cls.asset.pk, 'date': timezone.now().date() - timezone.timedelta(weeks=6), 'next_maintenance': timezone.now().date() + timezone.timedelta(weeks=20), 'current_usage': 800, 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.AVAILABLE, 'notes': 'maintenance event 1'}

    ## Test asset maintenance serializer with empty data
    def test_asset_maintenance_serializer_empty_data(self):
        serializer = AssetMaintenanceSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('asset', serializer.errors)
        self.assertIn('current_usage', serializer.errors)

    ## Test asset maintenance serializer with long data
    def test_asset_maintenance_serializer_long_data(self):
        serializer = AssetMaintenanceSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('current_usage', serializer.errors)
        self.assertIn('notes', serializer.errors)

    ## Test asset maintenance serializer with negative data
    def test_asset_maintenance_serializer_negative_data(self):
        serializer = AssetMaintenanceSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('current_usage', serializer.errors)

    ## Test asset maintenance serializer with invalid date data
    def test_asset_maintenance_serializer_invalid_date_data(self):
        serializer = AssetMaintenanceSerializer(data=self.invalid_date_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date', serializer.errors)

    ## Test asset maintenance serializer with valid data
    def test_asset_maintenance_serializer_valid_data(self):
        serializer = AssetMaintenanceSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('asset', serializer.validated_data)
        self.assertIn('notes', serializer.validated_data)

class TestAssetView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 'a' * 501
        cls.empty_data = {'name': '', 'serial_number': '', 'description': '', 'unit_cost': '', 'rental_cost': '', 'last_maintenance': '', 'next_maintenance': '', 'usage': '', 'location': '', 'condition': '', 'status': '', 'notes': ''}
        cls.short_data = {'name': 't', 'serial_number': '1', 'description': 'test', 'unit_cost': 0.0, 'rental_cost': 0.0, 'usage': 0.0, 'location': 'test', 'condition': 'good', 'status': 'available', 'notes': 'test'}
        cls.long_data = {'name': cls.long_string, 'serial_number': cls.long_string, 'description': cls.long_string, 'unit_cost': 0.0, 'rental_cost': 0.0, 'usage': 0.0, 'location': cls.long_string, 'condition': cls.long_string, 'status': cls.long_string, 'notes': cls.long_string}
        cls.negative_data = {'name': 'name', 'serial_number': '1', 'description': 'test', 'unit_cost': -5.65, 'rental_cost': -8.62, 'usage': -94.14, 'location': 'location', 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.IN_USE, 'notes': 'test'}
        cls.invalid_date_data = {'name': 'name', 'serial_number': '1', 'description': 'test', 'unit_cost': 5.65, 'rental_cost': 8.62, 'last_maintenance': timezone.now().date(), 'next_maintenance': timezone.now().date() - timezone.timedelta(weeks=26), 'usage': 94.14, 'location': 'location', 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.IN_USE, 'notes': 'test'}
        cls.create_data = {'name': 'name', 'serial_number': '1', 'description': 'test', 'unit_cost': 5.65, 'rental_cost': 8.62, 'last_maintenance': timezone.now().date(), 'next_maintenance': timezone.now().date() + timezone.timedelta(weeks=26), 'usage': 94.14, 'location': 'location', 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.IN_USE, 'notes': 'test'}
        cls.patch_data = {'name': 'updated name', 'description': 'updated description'}
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))
        cls.asset = Asset.objects.create(name='asset', serial_number='12942034', description='asset description', unit_cost=12.30, rental_cost=14.25, last_maintenance=timezone.now().date() - timezone.timedelta(weeks=6), next_maintenance=timezone.now().date() + timezone.timedelta(weeks=20), usage=500.00, location='location', condition=Asset.CONDITION_CHOICES.GOOD, status=Asset.STATUS_CHOICES.AVAILABLE, notes='asset notes')
        cls.list_url = reverse('asset-list')
        cls.detail_url = lambda pk: reverse('asset-detail', kwargs={'pk': pk})

    ## Test get asset not found
    def test_get_asset_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(96))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Asset Not Found.')

    ## Test get asset success
    def test_get_asset_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.asset.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.asset.name)
        self.assertEqual(response.data['serial_number'], self.asset.serial_number)
        self.assertEqual(response.data['description'], self.asset.description)
        self.assertEqual(float(response.data['unit_cost']), self.asset.unit_cost)
        self.assertEqual(float(response.data['rental_cost']), self.asset.rental_cost)
        self.assertEqual(response.data['last_maintenance'], self.asset.last_maintenance.isoformat())
        self.assertEqual(response.data['next_maintenance'], self.asset.next_maintenance.isoformat())
        self.assertEqual(float(response.data['usage']), self.asset.usage)
        self.assertEqual(response.data['location'], self.asset.location)
        self.assertEqual(response.data['condition'], self.asset.condition)
        self.assertEqual(response.data['status'], self.asset.status)
        self.assertEqual(response.data['notes'], self.asset.notes)

    ## Test get assets success
    def test_get_assets_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Asset.objects.count())

    ## Test create asset with empty data
    def test_create_asset_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('serial_number', response.data)

    ## Test create asset with short data
    def test_create_asset_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test create asset with long data
    def test_create_asset_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('serial_number', response.data)
        self.assertIn('description', response.data)
        self.assertIn('location', response.data)
        self.assertIn('condition', response.data)
        self.assertIn('status', response.data)
        self.assertIn('notes', response.data)

    ## Test create asset with negative data
    def test_create_asset_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('unit_cost', response.data)
        self.assertIn('rental_cost', response.data)
        self.assertIn('usage', response.data)

    ## Test create asset with invalid date data
    def test_create_asset_invalid_date_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.invalid_date_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('next_maintenance', response.data)

    ## Test create asset success
    def test_create_asset_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Asset.objects.count(), 2)
        asset = Asset.objects.get(name=self.create_data['name'])
        self.assertEqual(asset.name, self.create_data['name'])
        self.assertEqual(asset.serial_number, self.create_data['serial_number'])
        self.assertEqual(asset.description, self.create_data['description'])
        self.assertEqual(float(asset.unit_cost), self.create_data['unit_cost'])
        self.assertEqual(float(asset.rental_cost), self.create_data['rental_cost'])
        self.assertEqual(asset.last_maintenance, self.create_data['last_maintenance'])
        self.assertEqual(asset.next_maintenance, self.create_data['next_maintenance'])
        self.assertEqual(float(asset.usage), self.create_data['usage'])
        self.assertEqual(asset.location, self.create_data['location'])
        self.assertEqual(asset.condition, self.create_data['condition'])
        self.assertEqual(asset.status, self.create_data['status'])
        self.assertEqual(asset.notes, self.create_data['notes'])

    ## Test update asset with empty data
    def test_update_asset_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.asset.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('serial_number', response.data)

    ## Test update asset with short data
    def test_update_asset_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.asset.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test update asset with long data
    def test_update_asset_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.asset.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('serial_number', response.data)
        self.assertIn('description', response.data)
        self.assertIn('location', response.data)
        self.assertIn('condition', response.data)
        self.assertIn('status', response.data)
        self.assertIn('notes', response.data)

    ## Test update asset with negative data
    def test_update_asset_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.asset.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('unit_cost', response.data)
        self.assertIn('rental_cost', response.data)
        self.assertIn('usage', response.data)

    ## Test update asset with invalid date data
    def test_update_asset_invalid_date_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.asset.pk), data=self.invalid_date_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('next_maintenance', response.data)

    ## Test update asset success
    def test_update_asset_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.asset.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        asset = Asset.objects.get(pk=self.asset.pk)
        self.assertEqual(asset.name, self.patch_data['name'])
        self.assertEqual(asset.description, self.patch_data['description'])

    ## Test delete asset success
    def test_delete_asset_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.asset.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Asset.objects.count(), 0)

class TestAssetMaintenanceView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 'a' * 501
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))
        cls.asset = Asset.objects.create(name='asset', serial_number='12942034', description='asset description', unit_cost=12.30, rental_cost=14.25, last_maintenance=timezone.now().date() - timezone.timedelta(weeks=6), next_maintenance=timezone.now().date() + timezone.timedelta(weeks=20), usage=500.00, location='location', condition=Asset.CONDITION_CHOICES.GOOD, status=Asset.STATUS_CHOICES.AVAILABLE, notes='asset notes')
        cls.maintenance = AssetMaintenance.objects.create(asset=cls.asset, date=timezone.now().date() - timezone.timedelta(weeks=6), next_maintenance=timezone.now().date() + timezone.timedelta(weeks=20), current_usage=500, condition=Asset.CONDITION_CHOICES.GOOD, status=Asset.STATUS_CHOICES.AVAILABLE, notes='maintenance event')
        cls.empty_data = {'asset': '', 'date': '', 'next_maintenance': '', 'current_usage': '', 'condition': '', 'status': '', 'notes': ''}
        cls.long_data = {'asset': cls.asset.pk, 'date': timezone.now().date() - timezone.timedelta(weeks=6), 'next_maintenance': timezone.now().date() + timezone.timedelta(weeks=20), 'current_usage': 6105156165165156156181156156165800, 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.AVAILABLE, 'notes': cls.long_string}
        cls.negative_data = {'asset': cls.asset.pk, 'date': timezone.now().date() - timezone.timedelta(weeks=32), 'next_maintenance': timezone.now().date() - timezone.timedelta(weeks=6), 'current_usage': -250, 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.AVAILABLE, 'notes': 'maintenance event 1'}
        cls.invalid_date_data = {'asset': cls.asset.pk, 'date': timezone.now().date() - timezone.timedelta(weeks=6), 'next_maintenance': timezone.now().date() - timezone.timedelta(weeks=20), 'current_usage': 250, 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.AVAILABLE, 'notes': 'maintenance event 1'}
        cls.create_data = {'asset': cls.asset.pk, 'date': timezone.now().date() - timezone.timedelta(weeks=6), 'next_maintenance': timezone.now().date() + timezone.timedelta(weeks=20), 'current_usage': 800, 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.AVAILABLE, 'notes': 'maintenance event 1'}
        cls.patch_data = {'date': timezone.now().date(), 'notes': 'updated description'}
        cls.list_url = lambda asset_pk: reverse('asset-maintenance-list', kwargs={'asset_pk': asset_pk})
        cls.detail_url = lambda asset_pk, maintenance_pk: reverse('asset-maintenance-detail', kwargs={'asset_pk': asset_pk, 'maintenance_pk': maintenance_pk})

    ## Test get asset maintenance not found
    def test_get_asset_maintenance_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.asset.pk, 96))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Asset Maintenance Not Found.')

    ## Test get asset maintenance success
    def test_get_asset_maintenance_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.asset.pk, self.maintenance.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['asset'], self.maintenance.asset.pk)
        self.assertEqual(response.data['date'], self.maintenance.date.isoformat())
        self.assertEqual(response.data['next_maintenance'], self.maintenance.next_maintenance.isoformat())
        self.assertEqual(float(response.data['current_usage']), self.maintenance.current_usage)
        self.assertEqual(response.data['condition'], self.maintenance.condition)
        self.assertEqual(response.data['status'], self.maintenance.status)
        self.assertEqual(response.data['notes'], self.maintenance.notes)

    ## Test get asset maintenances success
    def test_get_asset_maintenances_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url(self.asset.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), AssetMaintenance.objects.count())

    ## Test create asset maintenance with empty data
    def test_create_asset_maintenance_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.asset.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('asset', response.data)

    ## Test create asset maintenance with long data
    def test_create_asset_maintenance_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.asset.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('current_usage', response.data)
        self.assertIn('notes', response.data)

    ## Test create asset maintenance with negative data
    def test_create_asset_maintenance_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.asset.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('current_usage', response.data)

    ## Test create asset maintenance with invalid date data
    def test_create_asset_maintenance_invalid_date_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.asset.pk), data=self.invalid_date_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)

    ## Test create asset maintenance success
    def test_create_asset_maintenance_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.asset.pk), data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AssetMaintenance.objects.count(), 2)
        maintenance = AssetMaintenance.objects.get(asset__pk=self.create_data['asset'], date=self.create_data['date'], notes=self.create_data['notes'])
        self.assertEqual(maintenance.asset.pk, self.create_data['asset'])
        self.assertEqual(maintenance.date, self.create_data['date'])
        self.assertEqual(maintenance.next_maintenance, self.create_data['next_maintenance'])
        self.assertEqual(float(maintenance.current_usage), self.create_data['current_usage'])
        self.assertEqual(maintenance.condition, self.create_data['condition'])
        self.assertEqual(maintenance.status, self.create_data['status'])
        self.assertEqual(maintenance.notes, self.create_data['notes'])

    ## Test update asset maintenance with empty data
    def test_update_asset_maintenance_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.asset.pk, self.maintenance.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('asset', response.data)

    ## Test update asset maintenance with long data
    def test_update_asset_maintenance_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.asset.pk, self.maintenance.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('current_usage', response.data)
        self.assertIn('notes', response.data)

    ## Test update asset maintenance with negative data
    def test_update_asset_maintenance_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.asset.pk, self.maintenance.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('current_usage', response.data)

    ## Test update asset maintenance with invalid date data
    def test_update_asset_maintenance_invalid_date_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.asset.pk, self.maintenance.pk), data=self.invalid_date_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)

    ## Test update asset maintenance success
    def test_update_asset_maintenance_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.asset.pk, self.maintenance.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        asset = AssetMaintenance.objects.get(pk=self.asset.pk)
        self.assertEqual(asset.date, self.patch_data['date'])
        self.assertEqual(asset.notes, self.patch_data['notes'])

    ## Test delete asset maintenance success
    def test_delete_asset_maintenance_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.asset.pk, self.maintenance.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AssetMaintenance.objects.count(), 0)
