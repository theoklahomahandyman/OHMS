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
        cls.asset = Asset.objects.create(name='asset', serial_number='12942034', description='asset description', unit_cost=12.30, rental_cost=14.25, last_maintenance=timezone.now().date() - timezone.timedelta(weeks=6), next_maintenance=timezone.now().date() + timezone.timedelta(weeks=20), usage=500, location='location', condition=Asset.CONDITION_CHOICES.GOOD, status=Asset.STATUS_CHOICES.AVAILABLE, notes='asset notes')
        cls.maintenance = AssetMaintenance.objects.create(asset=cls.asset, date=timezone.now().date() - timezone.timedelta(weeks=6), next_maintenance=timezone.now().date() + timezone.timedelta(weeks=20), current_usage=500, condition=Asset.CONDITION_CHOICES.GOOD, status=Asset.STATUS_CHOICES.AVAILABLE, notes='maintenance event 1')
        cls.old_data = AssetMaintenance.objects.create(asset=cls.asset, date=timezone.now().date() - timezone.timedelta(weeks=32), next_maintenance=timezone.now().date() - timezone.timedelta(weeks=6), current_usage=250, condition=Asset.CONDITION_CHOICES.GOOD, status=Asset.STATUS_CHOICES.AVAILABLE, notes='maintenance event 1')
        cls.empty_data = {'asset': '', 'date': '', 'next_maintenance': '', 'current_usage': '', 'condition': '', 'status': '', 'notes': ''}
        cls.negative_data = {'asset': cls.asset.pk, 'date': timezone.now().date() - timezone.timedelta(weeks=32), 'next_maintenance': timezone.now().date() - timezone.timedelta(weeks=6), 'current_usage': -250, 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.AVAILABLE, 'notes': 'maintenance event 1'}
        cls.invalid_date_data = {'asset': cls.asset.pk, 'date': timezone.now().date() - timezone.timedelta(weeks=6), 'next_maintenance': timezone.now().date() - timezone.timedelta(weeks=20), 'current_usage': 250, 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.AVAILABLE, 'notes': 'maintenance event 1'}
        cls.valid_data = {'asset': cls.asset.pk, 'date': timezone.now().date() - timezone.timedelta(weeks=6), 'next_maintenance': timezone.now().date() + timezone.timedelta(weeks=20), 'current_usage': 800, 'condition': Asset.CONDITION_CHOICES.GOOD, 'status': Asset.STATUS_CHOICES.AVAILABLE, 'notes': 'maintenance event 1'}

    ## Test asset maintenance serializer with empty data
    def test_asset_maintenance_serializer_empty_data(self):
        serializer = AssetMaintenanceSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('asset', serializer.errors)
        self.assertIn('current_usage', serializer.errors)

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
