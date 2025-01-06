from order.serializers import OrderSerializer, OrderCostSerializer, OrderPictureSerializer, OrderMaterialSerializer, OrderToolSerializer, OrderPaymentSerializer, OrderWorkerSerializer
from order.models import Order, OrderWorkLog, OrderCost, OrderPicture, OrderMaterial, OrderTool, OrderPayment, OrderWorker
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from purchase.models import Purchase, PurchaseMaterial
from supplier.models import Supplier, SupplierAddress
from django.contrib.auth.hashers import make_password
from django.contrib.staticfiles.finders import find
from django.core.exceptions import ValidationError
from rest_framework.fields import DateTimeField
# from asset.models import Asset, AssetInstance
from customer.models import Customer
from material.models import Material
from service.models import Service
from django.utils import timezone
from rest_framework import status
from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from tool.models import Tool
from user.models import User
import shutil

# Tests for order modesl
class TestOrderModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.date = timezone.now().date()
        cls.password = 'test12345'
        cls.picture_path = 'pergola-stain.jpg'
        cls.image = SimpleUploadedFile(name=cls.picture_path, content=open(find(cls.picture_path), 'rb').read(), content_type='image/jpg')
        cls.supplier = Supplier.objects.create(name='supplier')
        cls.address = SupplierAddress.objects.create(supplier=cls.supplier, street_address='123 Test Street', city='City', state='State', zip=12345)
        cls.material = Material.objects.create(name='material', size='2 inch X 4 inch X 8 feet', unit_cost=35.0, available_quantity=100)
        cls.tool = Tool.objects.create(name='tool', unit_cost=35.0, available_quantity=100)
        # cls.asset = Asset.objects.create(name='asset', description='asset description', notes='asset notes')
#         cls.instance = AssetInstance.objects.create(asset=cls.asset, serial_number='1283930', unit_cost=12.30, rental_cost=14.25, last_maintenance=timezone.now().date() - timezone.timedelta(weeks=6), next_maintenance=timezone.now().date() + timezone.timedelta(weeks=20), usage=500, location='location', condition=AssetInstance.CONDITION_CHOICES.GOOD, notes='instance notes')
        cls.purchase = Purchase.objects.create(supplier=cls.supplier, supplier_address=cls.address, tax=6.83, total=6.83, date=cls.date)
        cls.purchase_material = PurchaseMaterial.objects.create(purchase=cls.purchase, material=cls.material, quantity=10, cost=100.0)
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=103.0, hours_worked=12, material_upcharge=20.5, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.order_cost = OrderCost.objects.create(order=cls.order, name='test line item charge', cost=55.68)
        cls.order_picture = OrderPicture.objects.create(order=cls.order, image=cls.image)
        cls.order_material = OrderMaterial.objects.create(order=cls.order, material=cls.material, quantity=10.0)
        cls.order_tool = OrderTool.objects.create(order=cls.order, tool=cls.tool, quantity_used=10, quantity_broken=2)
        # cls.order_asset = OrderAsset.objects.create(order=cls.order, instance=cls.instance, usage=5.34, condition=AssetInstance.CONDITION_CHOICES.MAINTENANCE_SOON)
        cls.order_payment = OrderPayment.objects.create(order=cls.order, date=cls.date, type=OrderPayment.PAYMENT_CHOICES.CASH, total=cls.order.total, notes='test order payment')
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password), pay_rate=16.55)
        cls.order_worker = OrderWorker.objects.create(order=cls.order, user=cls.user)

    ## Test save method in the Order model
    def test_order_save(self):
        self.order.hourly_rate = 120.0
        self.order.hours_worked = 10
        self.order.material_upcharge = 15.0
        self.order.tax = 10.0
        self.order.discount = 5.0
        self.order.save()
        labor_costs = self.order.hourly_rate * self.order.hours_worked
        total_material_costs = self.material.unit_cost * self.order_material.quantity
        material_costs = total_material_costs * (1 + self.order.material_upcharge / 100)
        # asset_costs = self.instance.rental_cost * self.order_asset.usage
        order_costs = self.order_cost.cost
        subtotal = labor_costs + material_costs + order_costs + float(self.order.callout)
        tax_amount = (self.order.tax / 100) * subtotal
        discount_amount = (self.order.discount / 100) * subtotal
        expected_total = subtotal + tax_amount - discount_amount
        self.assertAlmostEqual(round(expected_total, 2), self.order.total, places=1)

    '''
        Test picture creation with image
        Verifies that the image is properly saved and exists after the picture is created.
    '''
    def test_order_picture_creation_with_image(self):
        # Verify image exists after creating a picture
        self.assertTrue(self.order_picture.image.storage.exists(self.order_picture.image.name))

    '''
        Test old picture image deletion on save
        Verifies that the old image is deleted and the new image is saved when updating a picture's image.
    '''
    def test_order_picture_image_deleted_on_save(self):
        old_image_name = self.order_picture.image.name
        new_image = SimpleUploadedFile(name='new-image.jpg', content=b'new_image_data', content_type='image/jpg')
        self.order_picture.image = new_image
        self.order_picture.save()
        self.order_picture.refresh_from_db()
        # Verify the old image is deleted
        self.assertFalse(self.order_picture.image.storage.exists(old_image_name))
        # Verify the new image is saved
        self.assertTrue(self.order_picture.image.storage.exists(self.order_picture.image.name))

    '''
        Test picture image deletion on delete
        Verifiess that the image is deleted from storage when the picture is deleted.
    '''
    def test_order_picture_image_deleted_on_delete(self):
        # Ensure the image exists in storage
        self.assertTrue(self.order_picture.image.storage.exists(self.order_picture.image.name))
        # Delete the picture and verify the image is removed
        self.order_picture.delete()
        self.assertFalse(self.order_picture.image.storage.exists(self.picture_path))

    ## Test Order Material save method
    def test_order_material_save(self):
        order_material = OrderMaterial(order=self.order, material=self.material, quantity=5)
        expected_quantity = self.material.available_quantity - order_material.quantity
        order_material.save()
        expected_price = self.material.unit_cost * order_material.quantity
        order_material.refresh_from_db()
        self.assertEqual(order_material.material.available_quantity, expected_quantity)
        self.assertAlmostEqual(order_material.quantity * self.material.unit_cost, expected_price, places=2)

    ## Test Order Tool save method
    def test_order_tool_save(self):
        order_tool = OrderTool(order=self.order, tool=self.tool, quantity_used=5, quantity_broken=2)
        order_tool.save()
        order_tool.refresh_from_db()
        self.assertEqual(order_tool.tool.available_quantity, self.tool.available_quantity)

    # ## Test Order Asset save method
    # def test_order_asset_save(self):
    #     order_asset = OrderAsset(order=self.order, instance=self.instance, usage=2.34, condition=AssetInstance.CONDITION_CHOICES.OUT_OF_SERVICE)
    #     order_asset.save()
    #     order_asset.refresh_from_db()
    #     self.assertAlmostEqual(float(order_asset.instance.usage), float(self.instance.usage), places=2)
    #     self.assertEqual(order_asset.instance.condition, order_asset.condition)

    ## Test Order Payment save method
    def test_order_payment_save(self):
        self.order_payment.order.save()
        self.order.refresh_from_db()
        self.assertTrue(self.order.paid)

    ## Test OrderWorkLog validation (start before end)
    def test_order_work_log_validation(self):
        order_work_log = OrderWorkLog(order=self.order, start=timezone.now(), end=timezone.now() - timezone.timedelta(hours=1))
        with self.assertRaises(ValidationError):
            order_work_log.save()

    ## Test OrderWorkLog validation success
    def test_order_work_log_validation_success(self):
        order_work_log = OrderWorkLog(order=self.order, start=timezone.now(), end=timezone.now() + timezone.timedelta(hours=6))
        order_work_log.save()
        self.assertAlmostEqual(self.order.hours_worked, 6)

    ## Test order calculate labor total
    def test_calculate_labor_total(self):
        self.order.hours_worked = 5
        self.order.hourly_rate = 100
        self.assertAlmostEqual(self.order.calculate_labor_total(), 500.0)

    ## Test order calculate material total
    def test_calculate_material_total(self):
        self.order.material_upcharge = 20
        self.assertAlmostEqual(self.order.calculate_material_total(), 120.0)

    ## Test order calculate line total
    def test_calculate_line_total(self):
        self.assertAlmostEqual(self.order.calculate_line_total(), 55.68)

    ## Test calculate tax total
    def test_calculate_tax_total(self):
        self.order.tax = 10
        self.assertAlmostEqual(self.order.calculate_tax_total(), (self.order.subtotal * 0.10))

    ## Test calculate discount total
    def test_calculate_discount_total(self):
        self.order.discount = 5
        self.assertAlmostEqual(self.order.calculate_discount_total(), (self.order.subtotal * 0.05))

    ## Test calculate total
    def test_calculate_total(self):
        self.order.save()
        self.assertAlmostEqual(self.order.calculate_total(), self.order.total)

    ## Test boolean field 'paid' determination
    def test_determine_paid(self):
        self.order.working_total = 0
        self.assertTrue(self.order.determine_paid())

    ## Test order worker save
    def test_order_worker_save(self):
        self.assertAlmostEqual(float(self.order_worker.total), float(self.user.pay_rate) * float(self.order.hours_worked), places=2)

# Tests for order serializer
class TestOrderSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.long_string = 't' * 10001
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=150.0, hours_worked=11.25, material_upcharge=19.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.picture = SimpleUploadedFile(name='pergola-stain.jpg', content=open(find('pergola-stain.jpg'), 'rb').read(), content_type='image/jpg')
        cls.empty_data = {'customer': '', 'date': '', 'description': '', 'service': '', 'hourly_rate': '', 'hours_worked': '', 'material_upcharge': '', 'tax': '', 'total': '', 'completed': '', 'paid': '', 'discount': '', 'notes': '', 'callout': ''}
        cls.short_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 't', 'service': cls.service.pk, 'hourly_rate': 50.25, 'hours_worked': 1.34, 'material_upcharge': 8.45, 'tax': 9.25, 'total': 0.0, 'completed': False, 'paid': False, 'discount': 0.0, 'notes': 'test notes', 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.long_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': cls.long_string, 'service': cls.service.pk, 'hourly_rate': 83.25, 'hours_worked': 6.25, 'material_upcharge': 90.23, 'tax': 26.78, 'total': 0.0, 'completed': False, 'paid': False, 'discount': 107.34, 'notes': cls.long_string, 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.negative_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 'test desctiption', 'service': cls.service.pk, 'hourly_rate': -83.25, 'hours_worked': -6.25, 'material_upcharge': -18.45, 'tax': -9.25, 'total': -55.28, 'completed': False, 'paid': False, 'discount': -8.34, 'notes': 'test notes', 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.valid_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 'test desctiption', 'service': cls.service.pk, 'hourly_rate': 83.25, 'hours_worked': 6.25, 'material_upcharge': 18.45, 'tax': 9.25, 'total': 0.0, 'completed': False, 'paid': False, 'discount': 0.0, 'notes': 'test notes', 'callout': Order.CALLOUT_CHOICES.STANDARD, 'uploaded_images': [cls.picture]}

    ## Test order serializer with empty data
    def test_order_serializer_empty_data(self):
        serializer = OrderSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('customer', serializer.errors)
        self.assertIn('date', serializer.errors)
        self.assertIn('description', serializer.errors)
        self.assertIn('service', serializer.errors)
        self.assertIn('hourly_rate', serializer.errors)
        self.assertIn('hours_worked', serializer.errors)
        self.assertIn('material_upcharge', serializer.errors)
        self.assertIn('tax', serializer.errors)
        self.assertIn('total', serializer.errors)
        self.assertIn('completed', serializer.errors)
        self.assertIn('paid', serializer.errors)
        self.assertIn('discount', serializer.errors)
        self.assertIn('callout', serializer.errors)

    ## Test order serializer with short data
    def test_order_serializer_short_data(self):
        serializer = OrderSerializer(data=self.short_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)
        self.assertIn('hourly_rate', serializer.errors)
        self.assertIn('hours_worked', serializer.errors)
        self.assertIn('material_upcharge', serializer.errors)

    ## Test order serializer with long data
    def test_order_serializer_long_data(self):
        serializer = OrderSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)
        self.assertIn('material_upcharge', serializer.errors)
        self.assertIn('tax', serializer.errors)
        self.assertIn('discount', serializer.errors)

    ## Test order serializer with negative data
    def test_order_serializer_negative_data(self):
        serializer = OrderSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('hourly_rate', serializer.errors)
        self.assertIn('hours_worked', serializer.errors)
        self.assertIn('material_upcharge', serializer.errors)
        self.assertIn('tax', serializer.errors)
        self.assertIn('total', serializer.errors)
        self.assertIn('discount', serializer.errors)

    ## Test order serializer validation success
    def test_order_serializer_validation_success(self):
        serializer = OrderSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('customer', serializer.validated_data)
        self.assertIn('date', serializer.validated_data)
        self.assertIn('description', serializer.validated_data)
        self.assertIn('service', serializer.validated_data)
        self.assertIn('hourly_rate', serializer.validated_data)
        self.assertIn('hours_worked', serializer.validated_data)
        self.assertIn('material_upcharge', serializer.validated_data)
        self.assertIn('tax', serializer.validated_data)
        self.assertIn('total', serializer.validated_data)
        self.assertIn('completed', serializer.validated_data)
        self.assertIn('paid', serializer.validated_data)
        self.assertIn('discount', serializer.validated_data)
        self.assertIn('callout', serializer.validated_data)

    def test_order_serializer_create(self):
        serializer = OrderSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.date, self.valid_data['date'])
        self.assertEqual(order.description, self.valid_data['description'])
        self.assertEqual(order.service, self.service)
        self.assertEqual(float(order.hourly_rate), self.valid_data['hourly_rate'])
        self.assertEqual(float(order.material_upcharge), self.valid_data['material_upcharge'])
        self.assertEqual(float(order.tax), self.valid_data['tax'])
        self.assertEqual(order.completed, self.valid_data['completed'])
        self.assertEqual(float(order.discount), self.valid_data['discount'])
        self.assertEqual(order.callout, self.valid_data['callout'])
        self.assertEqual(order.images.count(), 1)

    def test_order_serializer_update(self):
        new_image = SimpleUploadedFile(name='pergola-stain.jpg', content=open(find('pergola-stain.jpg'), 'rb').read(), content_type='image/jpg')
        update_data = {
            'customer': self.customer.pk,
            'date': timezone.now().date(),
            'description': 'test',
            'service': self.service.pk,
            'hourly_rate': 99,
            'tax': 10,
            'completed': True,
            'discount': 65,
            'uploaded_images': [new_image]
        }
        serializer = OrderSerializer(self.order, data=update_data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertEqual(order.description, 'test')
        self.assertEqual(order.hourly_rate, 99)
        self.assertEqual(order.tax, 10)
        self.assertEqual(order.completed, True)
        self.assertEqual(order.discount, 65)
        self.assertEqual(order.images.count(), 1)

# Tests for order cost serializer
class TestOrderCostSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.long_string = 't' * 301
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.order_cost = OrderCost.objects.create(order=cls.order, name='test line item charge', cost=55.68)
        cls.empty_data = {'order': '', 'name': '', 'cost': ''}
        cls.short_data = {'order': cls.order.pk, 'name': 't', 'cost': 24.99}
        cls.long_data = {'order': cls.order.pk, 'name': cls.long_string, 'cost': 24.99}
        cls.negative_data = {'order': cls.order.pk, 'name': 'test line item cost', 'cost': -24.99}
        cls.valid_data = {'order': cls.order.pk, 'name': 'test line item cost', 'cost': 24.99}

    ## Test order cost serializer with empty data
    def test_order_cost_serializer_empty_data(self):
        serializer = OrderCostSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)
        self.assertIn('name', serializer.errors)
        self.assertIn('cost', serializer.errors)

    ## Test order cost serializer with short data
    def test_order_cost_serializer_short_data(self):
        serializer = OrderCostSerializer(data=self.short_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test order cost serializer with long data
    def test_order_cost_serializer_long_data(self):
        serializer = OrderCostSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    ## Test order cost serializer with negative data
    def test_order_cost_serializer_negative_data(self):
        serializer = OrderCostSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('cost', serializer.errors)

    ## Test order cost serializer validation success
    def test_order_cost_serializer_validation_success(self):
        serializer = OrderCostSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('order', serializer.validated_data)
        self.assertIn('name', serializer.validated_data)
        self.assertIn('cost', serializer.validated_data)

# Tests for order picture serializer
class TestOrderPictureSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'
        )
        cls.image = SimpleUploadedFile(name='test_image.gif', content=cls.image_content, content_type='image/gif')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.order_picture = OrderPicture.objects.create(order=cls.order, image='pergola-stain.jpg')
        cls.empty_data = {'order': '', 'image': ''}
        cls.valid_data = {'order': cls.order.pk, 'image': cls.image}

    @classmethod
    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    ## Test order picture serializer with empty data
    def test_order_picture_serializer_empty_data(self):
        serializer = OrderPictureSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)
        self.assertIn('image', serializer.errors)

    ## Test order picture serializer validation success
    def test_order_picture_serializer_validation_success(self):
        serializer = OrderPictureSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('order', serializer.validated_data)
        self.assertIn('image', serializer.validated_data)

# Tests for order material serializer
class TestOrderMaterialSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.material = Material.objects.create(name='material', description='material description', size='size', unit_cost=12.99, available_quantity=12)
        cls.order_material = OrderMaterial.objects.create(order=cls.order, material=cls.material, quantity=10)
        cls.empty_data = {'order': '', 'material': '', 'quantity': ''}
        cls.negative_data = {'order': cls.order.pk, 'material': cls.material.pk, 'quantity': -10}
        cls.valid_data = {'order': cls.order.pk, 'material': cls.material.pk, 'quantity': 10}

    ## Test order material serializer with empty data
    def test_order_material_serializer_empty_data(self):
        serializer = OrderMaterialSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)
        self.assertIn('material', serializer.errors)
        self.assertIn('quantity', serializer.errors)

    ## Test order material serializer with negative data
    def test_order_material_serializer_negative_data(self):
        serializer = OrderMaterialSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    ## Test order material serializer validation success
    def test_order_material_serializer_validation_success(self):
        serializer = OrderMaterialSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('order', serializer.validated_data)
        self.assertIn('material', serializer.validated_data)
        self.assertIn('quantity', serializer.validated_data)

# Tests for order tool serializer
class TestOrderToolSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.tool = Tool.objects.create(name='tool', description='tool description', unit_cost=12.99, available_quantity=95)
        cls.order_tool = OrderTool.objects.create(order=cls.order, tool=cls.tool, quantity_used=10, quantity_broken=1)
        cls.empty_data = {'order': '', 'tool': '', 'quantity_used': '', 'quantity_broken': ''}
        cls.negative_data = {'order': cls.order.pk, 'tool': cls.tool.pk, 'quantity_used': -10, 'quantity_broken': -2}
        cls.valid_data = {'order': cls.order.pk, 'tool': cls.tool.pk, 'quantity_used': 10, 'quantity_broken': 2}

    ## Test order tool serializer with empty data
    def test_order_tool_serializer_empty_data(self):
        serializer = OrderToolSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)
        self.assertIn('tool', serializer.errors)
        self.assertIn('quantity_used', serializer.errors)
        self.assertIn('quantity_broken', serializer.errors)

    ## Test order tool serializer with negative data
    def test_order_tool_serializer_negative_data(self):
        serializer = OrderToolSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity_used', serializer.errors)
        self.assertIn('quantity_broken', serializer.errors)

    ## Test order tool serializer validation success
    def test_order_tool_serializer_validation_success(self):
        serializer = OrderToolSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('order', serializer.validated_data)
        self.assertIn('tool', serializer.validated_data)
        self.assertIn('quantity_used', serializer.validated_data)
        self.assertIn('quantity_broken', serializer.validated_data)

# # Tests for order asset serializer
# class TestOrderAssetSerializer(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.date = timezone.now().date()
#         cls.service = Service.objects.create(name='test service')
#         cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
#         cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
#         cls.asset = Asset.objects.create(name='asset', description='asset description', notes='asset notes')
#         cls.instance = AssetInstance.objects.create(asset=cls.asset, serial_number='1283930', unit_cost=12.30, rental_cost=14.25, last_maintenance=timezone.now().date() - timezone.timedelta(weeks=6), next_maintenance=timezone.now().date() + timezone.timedelta(weeks=20), usage=500, location='location', condition=AssetInstance.CONDITION_CHOICES.GOOD, notes='instance notes')
#         cls.empty_data = {'order': '', 'instance': '', 'usage': '', 'condition': ''}
#         cls.long_data = {'order': cls.order.pk, 'instance': cls.instance.pk, 'usage': 1516516165111444252152151561656.51, 'condition': 'a' * 18}
#         cls.negative_data = {'order': cls.order.pk, 'instance': cls.instance.pk, 'usage': -10.15, 'condition': AssetInstance.CONDITION_CHOICES.GOOD}
#         cls.valid_data = {'order': cls.order.pk, 'instance': cls.instance.pk, 'usage': 10.35, 'condition': AssetInstance.CONDITION_CHOICES.GOOD}

#     ## Test order asset serializer with empty data
#     def test_order_asset_serializer_empty_data(self):
#         serializer = OrderAssetSerializer(data=self.empty_data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn('order', serializer.errors)
#         self.assertIn('instance', serializer.errors)
#         self.assertIn('usage', serializer.errors)
#         self.assertIn('condition', serializer.errors)

#     ## Test order asset serializer with long data
#     def test_order_asset_serializer_long_data(self):
#         serializer = OrderAssetSerializer(data=self.long_data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn('condition', serializer.errors)

#     ## Test order asset serializer with negative data
#     def test_order_asset_serializer_negative_data(self):
#         serializer = OrderAssetSerializer(data=self.negative_data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn('usage', serializer.errors)

#     ## Test order asset serializer validation success
#     def test_order_asset_serializer_validation_success(self):
#         serializer = OrderAssetSerializer(data=self.valid_data)
#         self.assertTrue(serializer.is_valid())
#         self.assertIn('order', serializer.validated_data)
#         self.assertIn('instance', serializer.validated_data)
#         self.assertIn('usage', serializer.validated_data)
#         self.assertIn('condition', serializer.validated_data)

# Tests for order payment serializer
class TestOrderPaymentSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.long_string = 't' * 256
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.order_cost = OrderCost.objects.create(order=cls.order, name='test line item charge', cost=55.68)
        cls.material = Material.objects.create(name='material', description='material description', size='size', unit_cost=12.99, available_quantity=12)
        cls.order_material = OrderMaterial.objects.create(order=cls.order, material=cls.material, quantity=10)
        cls.order_payment = OrderPayment.objects.create(order=cls.order, date=cls.date, type=OrderPayment.PAYMENT_CHOICES.CHECK, total=cls.order.total, notes='test order payment')
        cls.empty_data = {'order': '', 'date': '', 'type': '', 'total': '', 'notes': ''}
        cls.long_data = {'order': cls.order.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CASH, 'total': cls.order.total, 'notes': cls.long_string}
        cls.negative_data = {'order': cls.order.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CASH, 'total': -65.38, 'notes': 'test notes'}
        cls.valid_data = {'order': cls.order.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CASH, 'total': cls.order.total, 'notes': 'test notes'}

    ## Test order payment serializer with empty data
    def test_order_payment_serializer_empty_data(self):
        serializer = OrderPaymentSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)
        self.assertIn('date', serializer.errors)
        self.assertIn('type', serializer.errors)
        self.assertIn('total', serializer.errors)

    ## Test order payment serializer with long data
    def test_order_payment_serializer_long_data(self):
        serializer = OrderPaymentSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('notes', serializer.errors)

    ## Test order payment serializer with negative data
    def test_order_payment_serializer_negative_data(self):
        serializer = OrderPaymentSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('total', serializer.errors)

    ## Test order payment serializer validation success
    def test_order_payment_serializer_validation_success(self):
        serializer = OrderPaymentSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('order', serializer.validated_data)
        self.assertIn('date', serializer.validated_data)
        self.assertIn('type', serializer.validated_data)
        self.assertIn('total', serializer.validated_data)
        self.assertIn('notes', serializer.validated_data)

# Tests for public view
class TestPublicView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.long_string = 'a' * 2001
        cls.date = timezone.now().date()
        cls.empty_customer_data = {'first_name': '', 'last_name': '', 'email': '', 'phone': '', 'date': cls.date, 'description': 'test description'}
        cls.short_customer_data = {'first_name': 'f', 'last_name': 'l', 'email': 't@e.com', 'phone': '12345678901', 'date': cls.date, 'description': 'test description'}
        cls.long_customer_data = {'first_name': cls.long_string, 'last_name': cls.long_string, 'email': f'{cls.long_string}@email.com', 'phone': cls.long_string, 'date': cls.date, 'description': 'test description'}
        cls.empty_order_data = {'first_name': 'first', 'last_name': 'last', 'email': 'test@email.com', 'phone': '1 (583) 201-3820', 'date': '', 'description': ''}
        cls.short_order_data = {'first_name': 'first', 'last_name': 'last', 'email': 'test@email.com', 'phone': '1 (583) 201-3820', 'date': '1', 'description': 't'}
        cls.long_order_data = {'first_name': 'first', 'last_name': 'last', 'email': 'test@email.com', 'phone': '1 (583) 201-3820', 'date': cls.long_string, 'description': cls.long_string}
        cls.create_data = {'first_name': 'first', 'last_name': 'last', 'email': 'firstlast@email.com', 'phone': '1 (405) 685-9354', 'date': cls.date, 'description': 'test desctiption'}
        cls.url = reverse('order-public')

    def test_public_customer_empty_data(self):
        response = self.client.post(self.url, data=self.empty_customer_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)

    def test_public_customer_short_data(self):
        response = self.client.post(self.url, data=self.short_customer_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)

    def test_public_customer_long_data(self):
        response = self.client.post(self.url, data=self.long_customer_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)

    def test_public_order_empty_data(self):
        response = self.client.post(self.url, data=self.empty_order_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)
        self.assertIn('description', response.data)

    def test_public_order_short_data(self):
        response = self.client.post(self.url, data=self.short_order_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)
        self.assertIn('description', response.data)

    def test_public_order_long_data(self):
        response = self.client.post(self.url, data=self.long_order_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)
        self.assertIn('description', response.data)

    def test_public_success(self):
        response = self.client.post(self.url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# Tests for order view
class TestOrderView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 'a' * 10001
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, material_upcharge=9.25, tax=13.5, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.empty_data = {'customer': '', 'date': '', 'description': '', 'service': '', 'hourly_rate': '', 'material_upcharge': '', 'tax': '', 'total': '', 'completed': '', 'discount': '', 'notes': '', 'callout': ''}
        cls.short_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 't', 'service': cls.service.pk, 'hourly_rate': 50.25, 'material_upcharge': 8.45, 'tax': 9.25, 'completed': False, 'discount': 0.0, 'notes': 'test notes', 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.long_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': cls.long_string, 'service': cls.service.pk, 'hourly_rate': 83.25, 'material_upcharge': 90.23, 'tax': 26.78, 'completed': False, 'discount': 107.34, 'notes': cls.long_string, 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.negative_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 'test desctiption', 'service': cls.service.pk, 'hourly_rate': -83.25, 'material_upcharge': -18.45, 'tax': -9.25, 'completed': False, 'discount': -8.34, 'notes': 'test notes', 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.create_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 'test desctiption', 'service': cls.service.pk, 'hourly_rate': 83.25, 'material_upcharge': 18.45, 'tax': 9.25, 'completed': False, 'discount': 0.0, 'notes': 'test notes', 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.patch_data = {'completed': True}
        cls.list_url = reverse('order-list')
        cls.detail_url = lambda pk: reverse('order-detail', kwargs={'pk': pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get order not found
    def test_get_order_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(79027269))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Order Not Found.')

    ## Test get order success
    def test_get_order_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer'], self.order.customer.pk)
        self.assertEqual(response.data['date'], self.order.date.strftime('%Y-%m-%d'))
        self.assertEqual(response.data['description'], self.order.description)
        self.assertEqual(response.data['service'], self.order.service.pk)
        self.assertEqual(float(response.data['hourly_rate']), self.order.hourly_rate)
        self.assertEqual(float(response.data['material_upcharge']), self.order.material_upcharge)
        self.assertEqual(float(response.data['tax']), self.order.tax)
        self.assertEqual(response.data['completed'], self.order.completed)
        self.assertEqual(float(response.data['discount']), self.order.discount)
        self.assertEqual(response.data['callout'], self.order.callout)

    ## Test get orders success
    def test_get_orders_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Order.objects.all().count())

    ## Test create order with empty data
    def test_create_order_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('customer', response.data)
        self.assertIn('description', response.data)
        self.assertIn('service', response.data)

    ## Test create order with short data
    def test_create_order_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
        self.assertIn('hourly_rate', response.data)
        self.assertIn('material_upcharge', response.data)

    ## Test create order with long data
    def test_create_order_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
        self.assertIn('material_upcharge', response.data)
        self.assertIn('tax', response.data)
        self.assertIn('discount', response.data)

    ## Test create order with negative data
    def test_create_order_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('hourly_rate', response.data)
        self.assertIn('material_upcharge', response.data)
        self.assertIn('tax', response.data)
        self.assertIn('discount', response.data)

    ## Test create order success
    def test_create_order_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        order = Order.objects.get(customer=self.create_data['customer'], description=self.create_data['description'], service=self.create_data['service'], callout=self.create_data['callout'])
        self.assertEqual(order.customer.pk, self.create_data['customer'])
        self.assertEqual(order.description, self.create_data['description'])
        self.assertEqual(order.service.pk, self.create_data['service'])
        self.assertEqual(float(order.hourly_rate), self.create_data['hourly_rate'])
        self.assertEqual(float(order.material_upcharge), self.create_data['material_upcharge'])
        self.assertEqual(float(order.tax), self.create_data['tax'])
        self.assertEqual(order.completed, self.create_data['completed'])
        self.assertEqual(float(order.discount), self.create_data['discount'])
        self.assertEqual(order.notes, self.create_data['notes'])

    ## Test update order with empty data
    def test_update_order_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('customer', response.data)
        self.assertIn('service', response.data)

    ## Test update order with short data
    def test_update_order_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
        self.assertIn('hourly_rate', response.data)
        self.assertIn('material_upcharge', response.data)

    ## Test update order with long data
    def test_update_order_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
        self.assertIn('material_upcharge', response.data)
        self.assertIn('tax', response.data)
        self.assertIn('discount', response.data)

    ## Test update order with negative data
    def test_update_order_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('hourly_rate', response.data)
        self.assertIn('material_upcharge', response.data)
        self.assertIn('tax', response.data)
        self.assertIn('discount', response.data)

    ## Test update order success
    def test_update_order_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order = Order.objects.get(pk=self.order.pk)
        self.assertEqual(order.completed, self.patch_data['completed'])

    ## Test delete order success
    def test_delete_order_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.order.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

# Tests for order work log view
class TestOrderWorkLogView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.order_work_log = OrderWorkLog.objects.create(order=cls.order, start=timezone.now() - timezone.timedelta(hours=16), end=timezone.now() - timezone.timedelta(hours=5))
        cls.empty_data = {'start': '', 'end': ''}
        cls.create_data = {'start': timezone.now() - timezone.timedelta(hours=6), 'end': timezone.now() - timezone.timedelta(hours=2)}
        cls.patch_data = {'end': timezone.now() + timezone.timedelta(hours=3)}
        cls.list_url = lambda order_pk: reverse('order-work-log-list', kwargs={'order_pk': order_pk})
        cls.detail_url = lambda order_pk, work_log_pk: reverse('order-work-log-detail', kwargs={'order_pk': order_pk, 'work_log_pk':work_log_pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get order work log not found
    def test_get_order_work_log_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk, 79027269))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Order Work Log Not Found.')

    ## Test get order work log success
    def test_get_order_work_log_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk, self.order_work_log.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dt_field = DateTimeField()
        expected_start = dt_field.to_representation(self.order_work_log.start)
        expected_end = dt_field.to_representation(self.order_work_log.end)
        self.assertEqual(response.data['order'], self.order_work_log.order.pk)
        self.assertEqual(response.data['start'], expected_start)
        self.assertEqual(response.data['end'], expected_end)

    ## Test get order work logs success
    def test_get_order_work_logs_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url(self.order.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), OrderWorkLog.objects.filter(order=self.order).count())

    ## Test create order work log with empty data
    def test_create_order_work_log_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start', response.data)
        self.assertIn('end', response.data)

    ## Test create order work log success
    def test_create_order_work_log_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderWorkLog.objects.count(), 2)
        work_log = OrderWorkLog.objects.get(order=self.order, start=self.create_data['start'], end=self.create_data['end'])
        self.assertEqual(work_log.order, self.order)
        self.assertEqual(work_log.start, self.create_data['start'])
        self.assertEqual(work_log.end, self.create_data['end'])

    ## Test update order work log with empty data
    def test_update_order_work_log_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_work_log.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start', response.data)
        self.assertIn('end', response.data)

    ## Test update order work log success
    def test_update_order_work_log_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_work_log.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        work_log = OrderWorkLog.objects.get(pk=self.order_work_log.pk)
        self.assertEqual(work_log.end, self.patch_data['end'])

    ## Test delete order work log success
    def test_delete_order_work_log_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.order.pk, self.order_work_log.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderWorkLog.objects.count(), 0)

# Tests for order cost view
class TestOrderCostView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 't' * 301
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.order_cost = OrderCost.objects.create(order=cls.order, name='test line item charge', cost=55.68)
        cls.empty_data = {'order': '', 'name': '', 'cost': ''}
        cls.short_data = {'order': cls.order.pk, 'name': 't', 'cost': 24.99}
        cls.long_data = {'order': cls.order.pk, 'name': cls.long_string, 'cost': 24.99}
        cls.negative_data = {'order': cls.order.pk, 'name': 'test line item cost', 'cost': -24.99}
        cls.create_data = {'order': cls.order.pk, 'name': 'test line item cost', 'cost': 24.99}
        cls.patch_data = {'name': 'updated test order cost'}
        cls.list_url = lambda order_pk: reverse('order-cost-list', kwargs={'order_pk': order_pk})
        cls.detail_url = lambda order_pk, cost_pk: reverse('order-cost-detail', kwargs={'order_pk': order_pk, 'cost_pk':cost_pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get order cost not found
    def test_get_order_cost_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk, 79027269))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Order Cost Not Found.')

    ## Test get order cost success
    def test_get_order_cost_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk, self.order_cost.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order'], self.order_cost.order.pk)
        self.assertEqual(response.data['name'], self.order_cost.name)
        self.assertEqual(float(response.data['cost']), self.order_cost.cost)

    ## Test get order costs success
    def test_get_order_costs_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url(self.order.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), OrderCost.objects.filter(order=self.order).count())

    ## Test create order cost with empty data
    def test_create_order_cost_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test create order cost with short data
    def test_create_order_cost_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test create order cost with long data
    def test_create_order_cost_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test create order cost with negative data
    def test_create_order_cost_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cost', response.data)

    ## Test create order cost success
    def test_create_order_cost_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderCost.objects.count(), 2)
        cost = OrderCost.objects.get(order=self.create_data['order'], name=self.create_data['name'], cost=self.create_data['cost'])
        self.assertEqual(cost.order.pk, self.create_data['order'])
        self.assertEqual(cost.name, self.create_data['name'])
        self.assertEqual(float(cost.cost), self.create_data['cost'])

    ## Test update order cost with empty data
    def test_update_order_cost_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_cost.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test update order cost with short data
    def test_update_order_cost_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_cost.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test update order cost with long data
    def test_update_order_cost_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_cost.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    ## Test update order cost with negative data
    def test_update_order_cost_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_cost.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cost', response.data)

    ## Test update order cost success
    def test_update_order_cost_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_cost.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cost = OrderCost.objects.get(pk=self.order_cost.pk)
        self.assertEqual(cost.name, self.patch_data['name'])

    ## Test delete order cost success
    def test_delete_order_cost_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.order.pk, self.order_cost.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderCost.objects.count(), 0)

# Tests for order picture view
class TestOrderPictureView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.date = timezone.now().date()
        cls.reciept_path = 'pergola-stain.jpg'
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.order_picture = OrderPicture.objects.create(order=cls.order, image=SimpleUploadedFile(name=cls.reciept_path, content=open(find(cls.reciept_path), 'rb').read(), content_type='image/jpg'))
        cls.detail_url = lambda pk: reverse('order-picture-detail', kwargs={'pk': pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    @classmethod
    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    ## Test delete order picture success
    def test_delete_order_picture_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.order_picture.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderPicture.objects.count(), 0)

# Tests for order material view
class TestOrderMaterialView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.material = Material.objects.create(name='material', description='material description', size='size', unit_cost=12.99, available_quantity=85)
        cls.order_material = OrderMaterial.objects.create(order=cls.order, material=cls.material, quantity=10)
        cls.empty_data = {'order': '', 'material': '', 'quantity': ''}
        cls.negative_data = {'order': cls.order.pk, 'material': cls.material.pk, 'quantity': -10}
        cls.create_data = {'order': cls.order.pk, 'material': cls.material.pk, 'quantity': 10}
        cls.patch_data = {'quantity': 45}
        cls.list_url = lambda order_pk: reverse('order-material-list', kwargs={'order_pk': order_pk})
        cls.detail_url = lambda order_pk, material_pk: reverse('order-material-detail', kwargs={'order_pk': order_pk, 'material_pk': material_pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get order material not found
    def test_get_order_material_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk, 79027269))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Order Material Not Found.')

    ## Test get order material success
    def test_get_order_material_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk, self.order_material.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order'], self.order_material.order.pk)
        self.assertEqual(response.data['material'], self.order_material.material.pk)
        self.assertEqual(response.data['quantity'], self.order_material.quantity)

    ## Test get order materials success
    def test_get_order_materials_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url(self.order.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), OrderMaterial.objects.filter(order=self.order).count())

    ## Test create order material with empty data
    def test_create_order_material_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('material', response.data)

    ## Test create order material with negative data
    def test_create_order_material_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('quantity', response.data)

    ## Test create order material success
    def test_create_order_material_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderMaterial.objects.count(), 2)

    ## Test update order material with empty data
    def test_update_order_material_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_material.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('material', response.data)

    ## Test update order material with negative data
    def test_update_order_material_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_material.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('quantity', response.data)

    ## Test update order material success
    def test_update_order_material_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_material.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        material = OrderMaterial.objects.get(pk=self.order_material.pk)
        self.assertEqual(material.quantity, self.patch_data['quantity'])

    ## Test delete order material success
    def test_delete_order_material_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.order.pk, self.order_material.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderMaterial.objects.count(), 0)

# Tests for order tool view
class TestOrderToolView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.tool = Tool.objects.create(name='tool', description='tool description', unit_cost=12.99, available_quantity=95)
        cls.order_tool = OrderTool.objects.create(order=cls.order, tool=cls.tool, quantity_used=10, quantity_broken=1)
        cls.empty_data = {'order': '', 'tool': '', 'quantity_used': '', 'quantity_broken': ''}
        cls.negative_data = {'order': cls.order.pk, 'tool': cls.tool.pk, 'quantity_used': -14, 'quantity_broken': -10}
        cls.create_data = {'order': cls.order.pk, 'tool': cls.tool.pk, 'quantity_used': 25, 'quantity_broken': 1}
        cls.patch_data = {'quantity_broken': 5}
        cls.list_url = lambda order_pk: reverse('order-tool-list', kwargs={'order_pk': order_pk})
        cls.detail_url = lambda order_pk, tool_pk: reverse('order-tool-detail', kwargs={'order_pk': order_pk, 'tool_pk': tool_pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get order tool not found
    def test_get_order_tool_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk, 79027269))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Order Tool Not Found.')

    ## Test get order tool success
    def test_get_order_tool_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk, self.order_tool.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order'], self.order_tool.order.pk)
        self.assertEqual(response.data['tool'], self.order_tool.tool.pk)
        self.assertEqual(response.data['quantity_used'], self.order_tool.quantity_used)
        self.assertEqual(response.data['quantity_broken'], self.order_tool.quantity_broken)

    ## Test get order tools success
    def test_get_order_tools_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url(self.order.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), OrderTool.objects.filter(order=self.order).count())

    ## Test create order tool with empty data
    def test_create_order_tool_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tool', response.data)

    ## Test create order tool with negative data
    def test_create_order_tool_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('quantity_used', response.data)
        self.assertIn('quantity_broken', response.data)

    ## Test create order tool success
    def test_create_order_tool_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderTool.objects.count(), 2)
        self.assertIn('order', response.data)
        self.assertIn('tool', response.data)
        self.assertIn('quantity_used', response.data)
        self.assertIn('quantity_broken', response.data)

    ## Test update order tool with empty data
    def test_update_order_tool_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_tool.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('order', response.data)
        self.assertIn('tool', response.data)

    ## Test update order tool with negative data
    def test_update_order_tool_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_tool.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('quantity_used', response.data)
        self.assertIn('quantity_broken', response.data)

    ## Test update order tool success
    def test_update_order_tool_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_tool.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tool = OrderTool.objects.get(pk=self.order_tool.pk)
        self.assertEqual(tool.quantity_broken, self.patch_data['quantity_broken'])

    ## Test delete order tool success
    def test_delete_order_tool_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.order.pk, self.order_tool.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderTool.objects.count(), 0)

# # Tests for order asset view
# class TestOrderAssetView(APITestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.client = APIClient()
#         cls.password = 'test1234'
#         cls.date = timezone.now().date()
#         cls.service = Service.objects.create(name='test service')
#         cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
#         cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
#         cls.asset = Asset.objects.create(name='asset', description='asset description', notes='asset notes')
#         cls.instance = AssetInstance.objects.create(asset=cls.asset, serial_number='1283930', unit_cost=12.30, rental_cost=14.25, last_maintenance=timezone.now().date() - timezone.timedelta(weeks=6), next_maintenance=timezone.now().date() + timezone.timedelta(weeks=20), usage=500, location='location', condition=AssetInstance.CONDITION_CHOICES.GOOD, notes='instance notes')
#         cls.order_asset = OrderAsset.objects.create(order=cls.order, instance=cls.instance, usage=4.24, condition=AssetInstance.CONDITION_CHOICES.GOOD)
#         cls.empty_data = {'order': '', 'instance': '', 'usage': '', 'condition': ''}
#         cls.long_data = {'order': cls.order.pk, 'instance': cls.instance.pk, 'usage': 15615135418513518351.25, 'condition': 'a' * 18}
#         cls.negative_data = {'order': cls.order.pk, 'instance': cls.instance.pk, 'usage': -14.51, 'condition': AssetInstance.CONDITION_CHOICES.GOOD}
#         cls.create_data = {'order': cls.order.pk, 'instance': cls.instance.pk, 'usage': 25.36, 'condition': AssetInstance.CONDITION_CHOICES.GOOD}
#         cls.patch_data = {'usage': 5.23, 'condition': AssetInstance.CONDITION_CHOICES.NEEDS_MAINTENANCE}
#         cls.list_url = lambda order_pk: reverse('order-asset-list', kwargs={'order_pk': order_pk})
#         cls.detail_url = lambda order_pk, asset_pk: reverse('order-asset-detail', kwargs={'order_pk': order_pk, 'asset_pk': asset_pk})
#         cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

#     ## Test get order asset not found
#     def test_get_order_asset_not_found(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(self.detail_url(self.order.pk, 79027269))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data['detail'], 'Order Asset Not Found.')

#     ## Test get order asset success
#     def test_get_order_asset_success(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(self.detail_url(self.order.pk, self.order_asset.pk))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['order'], self.order_asset.order.pk)
#         self.assertEqual(response.data['instance'], self.order_asset.instance.pk)
#         self.assertAlmostEqual(float(response.data['usage']), float(self.order_asset.usage), places=2)
#         self.assertEqual(response.data['condition'], self.order_asset.condition)

#     ## Test get order assets success
#     def test_get_order_assets_success(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(self.list_url(self.order.pk))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), OrderAsset.objects.filter(order=self.order).count())

#     ## Test create order asset with empty data
#     def test_create_order_asset_empty_data(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.post(self.list_url(self.order.pk), data=self.empty_data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('instance', response.data)
#         self.assertIn('usage', response.data)

#     ## Test create order asset with long data
#     def test_create_order_asset_long_data(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.post(self.list_url(self.order.pk), data=self.long_data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('usage', response.data)
#         self.assertIn('condition', response.data)

#     ## Test create order asset with negative data
#     def test_create_order_asset_negative_data(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.post(self.list_url(self.order.pk), data=self.negative_data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('usage', response.data)

#     ## Test create order asset success
#     def test_create_order_asset_success(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.post(self.list_url(self.order.pk), data=self.create_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(OrderAsset.objects.count(), 2)
#         self.assertIn('order', response.data)
#         self.assertIn('instance', response.data)
#         self.assertIn('usage', response.data)
#         self.assertIn('condition', response.data)

#     ## Test update order asset with empty data
#     def test_update_order_asset_empty_data(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.patch(self.detail_url(self.order.pk, self.order_asset.pk), data=self.empty_data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('order', response.data)
#         self.assertIn('instance', response.data)
#         self.assertIn('usage', response.data)

#     ## Test update order asset with long data
#     def test_update_order_asset_long_data(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.patch(self.detail_url(self.order.pk, self.order_asset.pk), data=self.long_data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('usage', response.data)
#         self.assertIn('condition', response.data)

#     ## Test update order asset with negative data
#     def test_update_order_asset_negative_data(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.patch(self.detail_url(self.order.pk, self.order_asset.pk), data=self.negative_data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('usage', response.data)

#     ## Test update order asset success
#     def test_update_order_asset_success(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.patch(self.detail_url(self.order.pk, self.order_asset.pk), data=self.patch_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         asset = OrderAsset.objects.get(pk=self.order_asset.pk)
#         self.assertAlmostEqual(float(asset.usage), float(self.patch_data['usage']), places=2)
#         self.assertEqual(asset.condition, self.patch_data['condition'])

#     ## Test delete order asset success
#     def test_delete_order_asset_success(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.delete(self.detail_url(self.order.pk, self.order_asset.pk))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(OrderAsset.objects.count(), 0)

# Tests for order payment view
class TestOrderPaymentView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 't' * 256
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.order_cost = OrderCost.objects.create(order=cls.order, name='test line item charge', cost=55.68)
        cls.material = Material.objects.create(name='material', description='material description', size='size', unit_cost=12.99, available_quantity=12)
        cls.order_material = OrderMaterial.objects.create(order=cls.order, material=cls.material, quantity=10)
        cls.order_payment = OrderPayment.objects.create(order=cls.order, date=cls.date, type=OrderPayment.PAYMENT_CHOICES.CHECK, total=cls.order.total, notes='test order payment')
        cls.empty_data = {'order': '', 'date': '', 'type': '', 'total': '', 'notes': ''}
        cls.long_data = {'order': cls.order.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CASH, 'total': cls.order.total, 'notes': cls.long_string}
        cls.negative_data = {'order': cls.order.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CASH, 'total': -65.38, 'notes': 'test notes'}
        cls.create_data = {'order': cls.order.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CASH, 'total': cls.order.total, 'notes': 'test notes'}
        cls.patch_data = {'notes': 'updated test order payment notes'}
        cls.list_url = lambda order_pk: reverse('order-payment-list', kwargs={'order_pk': order_pk})
        cls.detail_url = lambda order_pk, payment_pk: reverse('order-payment-detail', kwargs={'order_pk': order_pk, 'payment_pk':payment_pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get order payment not found
    def test_get_order_payment_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk, 79027269))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Order Payment Not Found.')

    ## Test get order payment success
    def test_get_order_payment_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk, self.order_payment.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order'], self.order_payment.order.pk)
        self.assertAlmostEqual(float(response.data['total']), self.order_payment.total, places=2)
        self.assertEqual(response.data['notes'], self.order_payment.notes)

    ## Test get order payments success
    def test_get_order_payments_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url(self.order.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), OrderPayment.objects.filter(order=self.order).count())

    ## Test create order payment with empty data
    def test_create_order_payment_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)
        self.assertIn('type', response.data)

    ## Test create order payment with long data
    def test_create_order_payment_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('notes', response.data)

    ## Test create order payment with negative data
    def test_create_order_payment_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('total', response.data)

    ## Test create order payment success
    def test_create_order_payment_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderPayment.objects.count(), 2)
        payment = OrderPayment.objects.get(order=self.create_data['order'], date=self.create_data['date'], type=self.create_data['type'], total=self.create_data['total'], notes=self.create_data['notes'])
        self.assertEqual(payment.order.pk, self.create_data['order'])
        self.assertEqual(payment.date, self.create_data['date'])
        self.assertEqual(payment.type, self.create_data['type'])
        self.assertEqual(float(payment.total), self.create_data['total'])
        self.assertEqual(payment.notes, self.create_data['notes'])

    ## Test update order payment with empty data
    def test_update_order_payment_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_payment.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('order', response.data)
        self.assertIn('date', response.data)
        self.assertIn('type', response.data)

    ## Test update order payment with long data
    def test_update_order_payment_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_payment.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('notes', response.data)

    ## Test update order payment with negative data
    def test_update_order_payment_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_payment.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('total', response.data)

    ## Test update order payment success
    def test_update_order_payment_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_payment.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment = OrderPayment.objects.get(pk=self.order_payment.pk)
        self.assertEqual(payment.notes, self.patch_data['notes'])

    ## Test delete order payment success
    def test_delete_order_payment_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.order.pk, self.order_payment.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderPayment.objects.count(), 0)


# Tests for order worker view
class TestOrderWorkerView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.long_string = 't' * 301
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.user1 = User.objects.create(first_name='first', last_name='user', email='firstuser@example.com', phone='1 (234) 567-8901', password=make_password(cls.password), pay_rate=21.32)
        cls.user2 = User.objects.create(first_name='second', last_name='user', email='seconduser@example.com', phone='1 (234) 567-8901', password=make_password(cls.password), pay_rate=21.32)
        cls.user3 = User.objects.create(first_name='third', last_name='user', email='thirduser@example.com', phone='1 (234) 567-8901', password=make_password(cls.password), pay_rate=21.32)
        cls.order_worker = OrderWorker.objects.create(order=cls.order, user=cls.user1)
        cls.empty_data = {'order': '', 'user': ''}
        cls.create_data = {'order': cls.order.pk, 'user': cls.user2.pk}
        cls.patch_data = {'user': cls.user3.pk}
        cls.list_url = lambda order_pk: reverse('order-worker-list', kwargs={'order_pk': order_pk})
        cls.detail_url = lambda order_pk, worker_pk: reverse('order-worker-detail', kwargs={'order_pk': order_pk, 'worker_pk':worker_pk})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test get order worker not found
    def test_get_order_worker_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk, 79027269))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Order Worker Not Found.')

    ## Test get order worker success
    def test_get_order_worker_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.order.pk, self.order_worker.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order'], self.order_worker.order.pk)
        self.assertEqual(response.data['user'], self.order_worker.user.pk)
        self.assertEqual(float(response.data['total']), self.order_worker.total)

    ## Test get order workers success
    def test_get_order_workers_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url(self.order.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), OrderWorker.objects.filter(order=self.order).count())

    ## Test create order worker with empty data
    def test_create_order_worker_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)

    ## Test create order worker success
    def test_create_order_worker_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(self.order.pk), data=self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderWorker.objects.count(), 2)
        worker = OrderWorker.objects.get(order=self.create_data['order'], user=self.create_data['user'])
        self.assertEqual(worker.order.pk, self.create_data['order'])
        self.assertEqual(worker.user.pk, self.create_data['user'])

    ## Test update order worker with empty data
    def test_update_order_worker_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_worker.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)

    ## Test update order worker success
    def test_update_order_worker_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk, self.order_worker.pk), data=self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        worker = OrderWorker.objects.get(pk=self.order_worker.pk)
        self.assertEqual(worker.user.pk, self.patch_data['user'])

    ## Test delete order worker success
    def test_delete_order_worker_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url(self.order.pk, self.order_worker.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderWorker.objects.count(), 0)
