from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from purchase.models import Purchase, PurchaseMaterial
from django.contrib.auth.hashers import make_password
from supplier.models import Supplier, SupplierAddress
from django.contrib.staticfiles.finders import find
from purchase.serializers import PurchaseSerializer
from material.models import Material
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for purchase models
class TestPurchaseModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)
        cls.purchase = Purchase.objects.create(supplier=cls.supplier, supplier_address=cls.address, tax=6.83, total=6.83, date='2024-08-01', reciept='pergola-stain.jpg')
        cls.material = Material.objects.create(name='material', size='2 inch X 4 inch X 8 feet', unit_cost=10.0, available_quantity=100)
        cls.purchase_material = PurchaseMaterial.objects.create(purchase=cls.purchase, material=cls.material, purchase_quantity=10, purchase_cost=100.0)

    ## Test string method for purchase model
    def test_purchase_string(self):
        self.assertEqual(str(self.purchase), f'OHMS{self.purchase.pk}-PUR')

    ## Test save method for purchase model
    def test_purchase_save(self):
        self.purchase.refresh_from_db()
        self.assertEqual(self.purchase.total, self.purchase.tax + self.purchase_material.purchase_cost)

    ## Test string method for purchase material model
    def test_purchase_material_string(self):
        self.assertEqual(str(self.purchase_material), f'{self.purchase_material.material.name} - {self.purchase_material.purchase_quantity} units purchased for ${self.purchase_material.purchase_cost}')

    ## Test save method for purchase material model
    def test_purchase_material_save(self):
        initial_quantity = self.material.available_quantity
        purchase_material = PurchaseMaterial.objects.create(purchase=self.purchase, material=self.material, purchase_quantity=10, purchase_cost=200.0)
        self.material.refresh_from_db()
        self.assertEqual(self.material.available_quantity, initial_quantity + purchase_material.purchase_quantity)
        ### Replacement method
        self.assertEqual(self.material.unit_cost, purchase_material.purchase_cost / purchase_material.purchase_quantity)
        self.purchase.refresh_from_db()
        purchase_materials = PurchaseMaterial.objects.filter(purchase=self.purchase)
        expected_total = self.purchase.tax + sum(purchase_material.purchase_cost for purchase_material in purchase_materials)
        self.assertAlmostEqual(self.purchase.total, expected_total, places=2)

    ## Test save method for purchase material model with zero quantity
    def test_purchase_material_save_zero_quantity(self):
        initial_quantity = self.material.available_quantity
        PurchaseMaterial.objects.create(purchase=self.purchase, material=self.material, purchase_quantity=0, purchase_cost=200.0)
        self.material.refresh_from_db()
        self.assertEqual(self.material.available_quantity, initial_quantity)
        self.assertEqual(self.material.unit_cost, 0.0)
        self.purchase.refresh_from_db()
        purchase_materials = PurchaseMaterial.objects.filter(purchase=self.purchase)
        expected_total = self.purchase.tax + sum(pm.purchase_cost for pm in purchase_materials)
        self.assertAlmostEqual(self.purchase.total, expected_total, places=2)

# Tests for purchase serializer
class TestPurchaseSerializer(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.reciept = SimpleUploadedFile(name='pergola-stain.jpg', content=open(find('pergola-stain.jpg'), 'rb').read(), content_type='image/jpg')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)
        cls.purchase = Purchase.objects.create(supplier=cls.supplier, supplier_address=cls.address, tax=6.83, total=6.83, date='2024-08-01', reciept='pergola-stain.jpg')
        cls.empty_data = {'supplier': '', 'supplier_address': '', 'tax': '', 'total': '', 'date': '', 'reciept': ''}
        cls.negative_data = {'supplier': cls.supplier.pk, 'supplier_address': cls.address.pk, 'tax': -6.78, 'total': -6.78, 'date': '2024-08-01', 'reciept': cls.reciept}
        cls.valid_data = {'supplier': cls.supplier.pk, 'supplier_address': cls.address.pk, 'tax': 6.78, 'total': 6.78, 'date': '2024-08-01', 'reciept': cls.reciept}

    ## Test purchase serializer with empty data
    def test_purchase_serializer_empty_data(self):
        serializer = PurchaseSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('supplier', serializer.errors)
        self.assertIn('supplier_address', serializer.errors)
        self.assertIn('date', serializer.errors)
        self.assertIn('reciept', serializer.errors)

    ## Test purchase serializer with negative data
    def test_purchase_serializer_negative_data(self):
        serializer = PurchaseSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tax', serializer.errors)
        self.assertIn('total', serializer.errors)

    ## Test purchase serializer validation success
    def test_purchase_serializer_validation_success(self):
        serializer = PurchaseSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('supplier', serializer.validated_data)
        self.assertIn('supplier_address', serializer.validated_data)
        self.assertIn('tax', serializer.validated_data)
        self.assertIn('total', serializer.validated_data)
        self.assertIn('date', serializer.validated_data)
        self.assertIn('reciept', serializer.validated_data)

class TestPurchaseView(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.reciept_path = 'pergola-stain.jpg'
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.reciept = SimpleUploadedFile(name=cls.reciept_path, content=open(find(cls.reciept_path), 'rb').read(), content_type='image/jpg')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)
        cls.purchase = Purchase.objects.create(supplier=cls.supplier, supplier_address=cls.address, tax=6.83, total=6.83, date='2024-08-01', reciept='pergola-stain.jpg')
        cls.empty_data = {'supplier': '', 'supplier_address': '', 'tax': '', 'total': '', 'date': '', 'reciept': ''}
        cls.negative_data = {'supplier': cls.supplier.pk, 'supplier_address': cls.address.pk, 'tax': -6.78, 'total': -6.78, 'date': '2024-08-01', 'reciept': cls.reciept}
        cls.create_data = {'supplier': cls.supplier.pk, 'supplier_address': cls.address.pk, 'tax': 6.78, 'total': 6.78, 'date': '2024-08-01', 'reciept': cls.reciept}
        cls.update_data = {'supplier': cls.supplier.pk, 'supplier_address': cls.address.pk, 'tax': 10.29, 'total': 10.29, 'date': '2024-03-05', 'reciept': cls.reciept}
        cls.patch_data = {'date': '2024-05-12'}
        cls.list_url = reverse('purchase-list')
        cls.detail_url = lambda pk: reverse('purchase-detail', kwargs={'pk': pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get purchase not found
    def test_get_purchase_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(96))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Purchase Not Found.')

    ## Test get purchase success
    def test_get_purchase_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.purchase.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['supplier'], self.purchase.supplier.pk)
        self.assertEqual(response.data['supplier_address'], self.purchase.supplier_address.pk)
        self.assertEqual(response.data['tax'], self.purchase.tax)
        self.assertEqual(response.data['total'], self.purchase.total)
        self.assertEqual(response.data['date'], self.purchase.date)
        self.assertEqual(response.data['reciept'], '/' + self.reciept_path)

    ## Test get purchases success
    def test_get_purchases_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Purchase.objects.count())

    ## Test create purchase with empty data
    def test_create_purchase_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('supplier', response.data)
        self.assertIn('supplier_address', response.data)
        self.assertIn('date', response.data)
        self.assertIn('reciept', response.data)

    ## Test create purchase with negative data
    def test_create_purchase_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tax', response.data)
        self.assertIn('total', response.data)

    ## Test create purchase success
    def test_create_purchase_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Purchase.objects.count(), 2)
        purchase = Purchase.objects.filter(supplier=self.create_data['supplier'], supplier_address=self.create_data['supplier_address'], date=self.create_data['date'], tax=self.create_data['tax'], total=self.create_data['total'])
        self.assertTrue(purchase.exists())

    ## Test update purchase with empty data
    def test_update_purchase_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url(self.purchase.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('supplier', response.data)
        self.assertIn('supplier_address', response.data)
        self.assertIn('date', response.data)
        self.assertIn('reciept', response.data)

    ## Test update purchase with negative data
    def test_update_purchase_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url(self.purchase.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tax', response.data)
        self.assertIn('total', response.data)

    ## Test update purchase success
    def test_update_purchase_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url(self.purchase.pk), data=self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        purchase = Purchase.objects.filter(supplier=self.update_data['supplier'], supplier_address=self.update_data['supplier_address'], date=self.update_data['date'], tax=self.update_data['tax'], total=self.update_data['total'])
        self.assertTrue(purchase.exists())

    ## Test partial update purchase with empty data
    def test_partial_update_purchase_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.purchase.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('supplier', response.data)
        self.assertIn('supplier_address', response.data)
        self.assertIn('date', response.data)
        self.assertIn('reciept', response.data)

    ## Test partial update purchase with negative data
    def test_partial_update_purchase_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.purchase.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tax', response.data)
        self.assertIn('total', response.data)

    ## Test partial update purchase success
    def test_partial_update_purchase_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.purchase.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        purchase = Purchase.objects.filter(date=self.patch_data['date'])
        self.assertTrue(purchase.exists())

    ## Test delete purchase success
    def test_delete_purchase_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.purchase.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Purchase.objects.count(), 0)
