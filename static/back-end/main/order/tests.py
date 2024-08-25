from order.serializers import OrderSerializer, OrderCostSerializer, OrderPictureSerializer, OrderMaterialSerializer, OrderPaymentSerializer
from order.models import Order, OrderCost, OrderPicture, OrderMaterial, OrderPayment
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from customer.models import Customer
from material.models import Material
from service.models import Service
from django.utils import timezone
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from user.models import User

# Tests for order modesl
class TestOrderModels(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=103.0, hours_worked=12, material_upcharge=20.5, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.order_cost = OrderCost.objects.create(order=cls.order, name='test line item charge', cost=55.68)
        cls.order_picture = OrderPicture.objects.create(order=cls.order, image='pergola-stain.jpg')
        cls.material = Material.objects.create(name='material', description='material description', size='size', unit_cost=12.99, available_quantity=12)
        cls.order_material = OrderMaterial.objects.create(order=cls.order, material=cls.material, quantity=10, price=240.99)
        cls.order_payment = OrderPayment.objects.create(order=cls.order, customer=cls.customer, date=cls.date, type=OrderPayment.PAYMENT_CHOICES.CASH, total=cls.order.total, notes='test order payment')

    ## Test order model save method and the use of the calculate_total method
    def test_order_save(self):
        self.order.hourly_rate = 120.0
        self.order.hours_worked = 10
        self.order.material_upcharge = 15.0
        self.order.tax = 10.0
        self.order.discount = 5.0
        self.order.save()
        labor_costs = self.order.hourly_rate * self.order.hours_worked
        total_material_costs = self.order_material.price
        material_costs = total_material_costs * (1 + self.order.material_upcharge / 100)
        order_costs = self.order_cost.cost
        subtotal = labor_costs + material_costs + order_costs + float(self.order.callout)
        tax_amount = (self.order.tax / 100) * subtotal
        discount_amount = (self.order.discount / 100) * subtotal
        expected_total = subtotal + tax_amount - discount_amount
        self.assertAlmostEqual(expected_total, self.order.total, places=2)

    ## Test order material model save method
    def test_order_material_save(self):
        order_material = OrderMaterial(order=self.order, material=self.material, quantity=5)
        order_material.save()
        expected_price = self.material.unit_cost * order_material.quantity
        order_material.refresh_from_db()
        self.assertAlmostEqual(order_material.price, expected_price, places=2)

    ## test order payment model save method
    def test_order_payment_save(self):
        self.assertTrue(self.order.paid)

# Tests for order serializer
class TestOrderSerializer(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.long_string = 't' * 10001
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=150.0, hours_worked=11.25, material_upcharge=19.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.empty_data = {'customer': '', 'date': '', 'description': '', 'service': '', 'hourly_rate': '', 'hours_worked': '', 'material_upcharge': '', 'tax': '', 'total': '', 'completed': '', 'paid': '', 'discount': '', 'notes': '', 'callout': ''}
        cls.short_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 't', 'service': cls.service.pk, 'hourly_rate': 50.25, 'hours_worked': 1.34, 'material_upcharge': 8.45, 'tax': 9.25, 'total': 0.0, 'completed': False, 'paid': False, 'discount': 0.0, 'notes': 'test notes', 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.long_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': cls.long_string, 'service': cls.service.pk, 'hourly_rate': 83.25, 'hours_worked': 6.25, 'material_upcharge': 90.23, 'tax': 26.78, 'total': 0.0, 'completed': False, 'paid': False, 'discount': 107.34, 'notes': cls.long_string, 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.negative_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 'test desctiption', 'service': cls.service.pk, 'hourly_rate': -83.25, 'hours_worked': -6.25, 'material_upcharge': -18.45, 'tax': -9.25, 'total': -55.28, 'completed': False, 'paid': False, 'discount': -8.34, 'notes': 'test notes', 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.valid_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 'test desctiption', 'service': cls.service.pk, 'hourly_rate': 83.25, 'hours_worked': 6.25, 'material_upcharge': 18.45, 'tax': 9.25, 'total': 0.0, 'completed': False, 'paid': False, 'discount': 0.0, 'notes': 'test notes', 'callout': Order.CALLOUT_CHOICES.STANDARD}

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
        cls.order_material = OrderMaterial.objects.create(order=cls.order, material=cls.material, quantity=10, price=240.99)
        cls.empty_data = {'order': '', 'material': '', 'quantity': '', 'price': ''}
        cls.negative_data = {'order': cls.order.pk, 'material': cls.material.pk, 'quantity': -10, 'price': -309.56}
        cls.valid_data = {'order': cls.order.pk, 'material': cls.material.pk, 'quantity': 10, 'price': 309.56}

    ## Test order material serializer with empty data
    def test_order_material_serializer_empty_data(self):
        serializer = OrderMaterialSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)
        self.assertIn('material', serializer.errors)
        self.assertIn('quantity', serializer.errors)
        self.assertIn('price', serializer.errors)

    ## Test order material serializer with negative data
    def test_order_material_serializer_negative_data(self):
        serializer = OrderMaterialSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)
        self.assertIn('price', serializer.errors)

    ## Test order material serializer validation success
    def test_order_material_serializer_validation_success(self):
        serializer = OrderMaterialSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('order', serializer.validated_data)
        self.assertIn('material', serializer.validated_data)
        self.assertIn('quantity', serializer.validated_data)
        self.assertIn('price', serializer.validated_data)

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
        cls.order_material = OrderMaterial.objects.create(order=cls.order, material=cls.material, quantity=10, price=240.99)
        cls.order_payment = OrderPayment.objects.create(order=cls.order, customer=cls.customer, date=cls.date, type=OrderPayment.PAYMENT_CHOICES, total=cls.order.total, notes='test order payment')
        cls.empty_data = {'order': '', 'customer': '', 'date': '', 'type': '', 'total': '', 'notes': ''}
        cls.long_data = {'order': cls.order.pk, 'customer': cls.customer.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CASH, 'total': cls.order.total, 'notes': cls.long_string}
        cls.negative_data = {'order': cls.order.pk, 'customer': cls.customer.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CASH, 'total': -65.38, 'notes': 'test notes'}
        cls.valid_data = {'order': cls.order.pk, 'customer': cls.customer.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CASH, 'total': cls.order.total, 'notes': 'test notes'}

    ## Test order payment serializer with empty data
    def test_order_payment_serializer_empty_data(self):
        serializer = OrderPaymentSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)
        self.assertIn('customer', serializer.errors)
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
        self.assertIn('customer', serializer.validated_data)
        self.assertIn('date', serializer.validated_data)
        self.assertIn('type', serializer.validated_data)
        self.assertIn('total', serializer.validated_data)
        self.assertIn('notes', serializer.validated_data)

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
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.empty_data = {'customer': '', 'date': '', 'description': '', 'service': '', 'hourly_rate': '', 'hours_worked': '', 'material_upcharge': '', 'tax': '', 'total': '', 'completed': '', 'paid': '', 'discount': '', 'notes': '', 'callout': ''}
        cls.short_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 't', 'service': cls.service.pk, 'hourly_rate': 50.25, 'hours_worked': 1.34, 'material_upcharge': 8.45, 'tax': 9.25, 'total': 0.0, 'completed': False, 'paid': False, 'discount': 0.0, 'notes': 'test notes', 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.long_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': cls.long_string, 'service': cls.service.pk, 'hourly_rate': 83.25, 'hours_worked': 6.25, 'material_upcharge': 90.23, 'tax': 26.78, 'total': 0.0, 'completed': False, 'paid': False, 'discount': 107.34, 'notes': cls.long_string, 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.negative_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 'test desctiption', 'service': cls.service.pk, 'hourly_rate': -83.25, 'hours_worked': -6.25, 'material_upcharge': -18.45, 'tax': -9.25, 'total': -55.28, 'completed': False, 'paid': False, 'discount': -8.34, 'notes': 'test notes', 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.create_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 'test desctiption', 'service': cls.service.pk, 'hourly_rate': 83.25, 'hours_worked': 6.25, 'material_upcharge': 18.45, 'tax': 9.25, 'total': 0.0, 'completed': False, 'paid': False, 'discount': 0.0, 'notes': 'test notes', 'callout': Order.CALLOUT_CHOICES.STANDARD}
        cls.update_data = {'customer': cls.customer.pk, 'date': cls.date, 'description': 'updated desctiption', 'service': cls.service.pk, 'hourly_rate': 183.25, 'hours_worked': 16.25, 'material_upcharge': 15.45, 'tax': 10.25, 'total': float(Order.CALLOUT_CHOICES.EMERGENCY), 'completed': False, 'paid': False, 'discount': 5.67, 'notes': 'updated test notes', 'callout': Order.CALLOUT_CHOICES.EMERGENCY}
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
        self.assertEqual(response.data['date'], f'{self.order.date.year}-0{self.order.date.month}-{self.order.date.day}')
        self.assertEqual(response.data['description'], self.order.description)
        self.assertEqual(response.data['service'], self.order.service.pk)
        self.assertEqual(response.data['hourly_rate'], self.order.hourly_rate)
        self.assertEqual(response.data['hours_worked'], self.order.hours_worked)
        self.assertEqual(response.data['material_upcharge'], self.order.material_upcharge)
        self.assertEqual(response.data['tax'], self.order.tax)
        self.assertEqual(response.data['total'], self.order.total)
        self.assertEqual(response.data['completed'], self.order.completed)
        self.assertEqual(response.data['paid'], self.order.paid)
        self.assertEqual(response.data['discount'], self.order.discount)
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
        self.assertIn('date', response.data)
        self.assertIn('description', response.data)
        self.assertIn('service', response.data)

    ## Test create order with short data
    def test_create_order_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
        self.assertIn('hourly_rate', response.data)
        self.assertIn('hours_worked', response.data)
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
        self.assertIn('hours_worked', response.data)
        self.assertIn('material_upcharge', response.data)
        self.assertIn('tax', response.data)
        self.assertIn('total', response.data)
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
        self.assertEqual(order.hourly_rate, self.create_data['hourly_rate'])
        self.assertEqual(order.hours_worked, self.create_data['hours_worked'])
        self.assertEqual(order.material_upcharge, self.create_data['material_upcharge'])
        self.assertEqual(order.tax, self.create_data['tax'])
        self.assertEqual(order.completed, self.create_data['completed'])
        self.assertEqual(order.paid, self.create_data['paid'])
        self.assertEqual(order.discount, self.create_data['discount'])
        self.assertEqual(order.notes, self.create_data['notes'])

    ## Test update order with empty data
    def test_update_order_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url(self.order.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('customer', response.data)
        self.assertIn('date', response.data)
        self.assertIn('description', response.data)
        self.assertIn('service', response.data)

    ## Test update order with short data
    def test_update_order_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url(self.order.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
        self.assertIn('hourly_rate', response.data)
        self.assertIn('hours_worked', response.data)
        self.assertIn('material_upcharge', response.data)

    ## Test update order with long data
    def test_update_order_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url(self.order.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
        self.assertIn('material_upcharge', response.data)
        self.assertIn('tax', response.data)
        self.assertIn('discount', response.data)

    ## Test update order with negative data
    def test_update_order_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url(self.order.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('hourly_rate', response.data)
        self.assertIn('hours_worked', response.data)
        self.assertIn('material_upcharge', response.data)
        self.assertIn('tax', response.data)
        self.assertIn('total', response.data)
        self.assertIn('discount', response.data)

    ## Test update order success
    def test_update_order_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url(self.order.pk), data=self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order = Order.objects.get(customer=self.update_data['customer'], description=self.update_data['description'], service=self.update_data['service'], callout=self.update_data['callout'])
        self.assertEqual(order.customer.pk, self.update_data['customer'])
        self.assertEqual(order.description, self.update_data['description'])
        self.assertEqual(order.service.pk, self.update_data['service'])
        self.assertEqual(order.hourly_rate, self.update_data['hourly_rate'])
        self.assertEqual(order.hours_worked, self.update_data['hours_worked'])
        self.assertEqual(order.material_upcharge, self.update_data['material_upcharge'])
        self.assertEqual(order.tax, self.update_data['tax'])
        self.assertEqual(order.completed, self.update_data['completed'])
        self.assertEqual(order.paid, self.update_data['paid'])
        self.assertEqual(order.discount, self.update_data['discount'])
        self.assertEqual(order.notes, self.update_data['notes'])

    ## Test partial update order with empty data
    def test_partial_update_order_empty_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk), data=self.empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('customer', response.data)
        self.assertIn('date', response.data)
        self.assertIn('description', response.data)
        self.assertIn('service', response.data)

    ## Test partial update order with short data
    def test_partial_update_order_short_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk), data=self.short_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
        self.assertIn('hourly_rate', response.data)
        self.assertIn('hours_worked', response.data)
        self.assertIn('material_upcharge', response.data)

    ## Test partial update order with long data
    def test_partial_update_order_long_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk), data=self.long_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
        self.assertIn('material_upcharge', response.data)
        self.assertIn('tax', response.data)
        self.assertIn('discount', response.data)

    ## Test partial update order with negative data
    def test_partial_update_order_negative_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url(self.order.pk), data=self.negative_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('hourly_rate', response.data)
        self.assertIn('hours_worked', response.data)
        self.assertIn('material_upcharge', response.data)
        self.assertIn('tax', response.data)
        self.assertIn('total', response.data)
        self.assertIn('discount', response.data)

    ## Test partial update order success
    def test_partial_update_order_success(self):
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
        cls.update_data = {'order': cls.order.pk, 'name': 'updated test line item cost', 'cost': 38.62}
        cls.patch_data = {'name': 'updated test order cost'}
        # cls.create_url = reverse('order-cost-create')
        # cls.list_url = lambda pk: reverse('order-cost-list', kwargs={'pk': pk, 'type': 'm'})
        # cls.detail_url = lambda pk: reverse('order-cost-detail', kwargs={'pk': pk, 'type':'s'})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))
        
    ## Test get order cost not found
    def test_get_order_cost_not_found(self):
        pass

    ## Test get order cost success
    def test_get_order_cost_success(self):
        pass

    ## Test get order costs success
    def test_get_order_costs_success(self):
        pass

    ## Test create order cost with empty data
    def test_create_order_cost_empty_data(self):
        pass

    ## Test create order cost with short data
    def test_create_order_cost_short_data(self):
        pass

    ## Test create order cost with long data
    def test_create_order_cost_long_data(self):
        pass

    ## Test create order cost with negative data
    def test_create_order_cost_negative_data(self):
        pass

    ## Test create order cost success
    def test_create_order_cost_success(self):
        pass

    ## Test update order cost with empty data
    def test_update_order_cost_empty_data(self):
        pass

    ## Test update order cost with short data
    def test_update_order_cost_short_data(self):
        pass

    ## Test update order cost with long data
    def test_update_order_cost_long_data(self):
        pass

    ## Test update order cost with negative data
    def test_update_order_cost_negative_data(self):
        pass

    ## Test update order cost success
    def test_update_order_cost_success(self):
        pass

    ## Test partial update order cost with empty data
    def test_partial_update_order_cost_empty_data(self):
        pass

    ## Test partial update order cost with short data
    def test_partial_update_order_cost_short_data(self):
        pass

    ## Test partial update order cost with long data
    def test_partial_update_order_cost_long_data(self):
        pass

    ## Test partial update order cost with negative data
    def test_partial_update_order_cost_negative_data(self):
        pass

    ## Test partial update order cost success
    def test_partial_update_order_cost_success(self):
        pass

    ## Test delete order cost success
    def test_delete_order_cost_success(self):
        pass

# Tests for order picture view
class TestOrderPictureView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.image_content_1 = (b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b')
        cls.image_content_2 = (b'\x47\x49\x46\x38\x39\x61\x02\x00\x02\x00\x80\x00\x00\x00\x00\x00\xff\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x02\x00\x02\x00\x00\x02\x04\x44\x11\x00\x3b')
        cls.image_content_3 = (b'\x47\x49\x46\x38\x39\x61\x03\x00\x03\x00\x80\x00\x00\xff\x00\x00\x00\xff\xff\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x03\x00\x03\x00\x00\x02\x06\x44\x11\x22\x00\x3b')
        cls.image_1 = SimpleUploadedFile(name='test_image_1.gif', content=cls.image_content_1, content_type='image/gif')
        cls.image_2 = SimpleUploadedFile(name='test_image_2.gif', content=cls.image_content_2, content_type='image/gif')
        cls.image_3 = SimpleUploadedFile(name='test_image_3.gif', content=cls.image_content_3, content_type='image/gif')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.order_picture = OrderPicture.objects.create(order=cls.order, image='pergola-stain.jpg')
        cls.empty_data = {'order': '', 'image': ''}
        cls.valid_data = {'order': cls.order.pk, 'image': cls.image_1}
        cls.update_data = {'order': cls.order.pk, 'image': cls.image_2}
        cls.patch_data = {'image': cls.image_3}
        # cls.create_url = reverse('order-picture-create')
        # cls.list_url = lambda pk: reverse('order-picture-list', kwargs={'pk': pk, 'type': 'm'})
        # cls.detail_url = lambda pk: reverse('order-picture-detail', kwargs={'pk': pk, 'type':'s'})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))
        
    ## Test get order picture not found
    def test_get_order_picture_not_found(self):
        pass

    ## Test get order picture success
    def test_get_order_picture_success(self):
        pass

    ## Test get order pictures success
    def test_get_order_pictures_success(self):
        pass

    ## Test create order picture with empty data
    def test_create_order_picture_empty_data(self):
        pass

    ## Test create order picture success
    def test_create_order_picture_success(self):
        pass

    ## Test update order picture with empty data
    def test_update_order_picture_empty_data(self):
        pass

    ## Test update order picture success
    def test_update_order_picture_success(self):
        pass

    ## Test partial update order picture with empty data
    def test_partial_update_order_picture_empty_data(self):
        pass

    ## Test partial update order picture success
    def test_partial_update_order_picture_success(self):
        pass

    ## Test delete order picture success
    def test_delete_order_picture_success(self):
        pass

# Tests for order material view
class TestOrderMatematerialView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.password = 'test1234'
        cls.date = timezone.now().date()
        cls.service = Service.objects.create(name='test service')
        cls.customer = Customer.objects.create(first_name='first', last_name='last', email='firstlast@email.com', phone='1 (234) 567-8901', notes='test customer')
        cls.order = Order.objects.create(customer=cls.customer, date=cls.date, description='test description', service=cls.service, hourly_rate=50.0, hours_worked=1.25, material_upcharge=9.25, tax=13.5, total=0.0, completed=False, paid=False, discount=1.75, notes='test order', callout=Order.CALLOUT_CHOICES.STANDARD)
        cls.material = Material.objects.create(name='material', description='material description', size='size', unit_cost=12.99, available_quantity=12)
        cls.order_material = OrderMaterial.objects.create(order=cls.order, material=cls.material, quantity=10, price=240.99)
        cls.empty_data = {'order': '', 'material': '', 'quantity': '', 'price': ''}
        cls.negative_data = {'order': cls.order.pk, 'material': cls.material.pk, 'quantity': -10, 'price': -309.56}
        cls.create_data = {'order': cls.order.pk, 'material': cls.material.pk, 'quantity': 10, 'price': 0}
        cls.update_data = {'order': cls.order.pk, 'material': cls.material.pk, 'quantity': 22, 'price': 0}
        cls.patch_data = {'quantity': 45}
        # cls.create_url = reverse('order-material-create')
        # cls.list_url = lambda pk: reverse('order-material-list', kwargs={'pk': pk, 'type': 'm'})
        # cls.detail_url = lambda pk: reverse('order-material-detail', kwargs={'pk': pk, 'type':'s'})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))
        
    ## Test get order material not found
    def test_get_order_material_not_found(self):
        pass

    ## Test get order material success
    def test_get_order_material_success(self):
        pass

    ## Test get order materials success
    def test_get_order_materials_success(self):
        pass

    ## Test create order material with empty data
    def test_create_order_material_empty_data(self):
        pass

    ## Test create order material with negative data
    def test_create_order_material_negative_data(self):
        pass

    ## Test create order material success
    def test_create_order_material_success(self):
        pass

    ## Test update order material with empty data
    def test_update_order_material_empty_data(self):
        pass

    ## Test update order material with negative data
    def test_update_order_material_negative_data(self):
        pass

    ## Test update order material success
    def test_update_order_material_success(self):
        pass

    ## Test partial update order material with empty data
    def test_partial_update_order_material_empty_data(self):
        pass

    ## Test partial update order material with negative data
    def test_partial_update_order_material_negative_data(self):
        pass

    ## Test partial update order material success
    def test_partial_update_order_material_success(self):
        pass

    ## Test delete order material success
    def test_delete_order_material_success(self):
        pass

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
        cls.order_material = OrderMaterial.objects.create(order=cls.order, material=cls.material, quantity=10, price=240.99)
        cls.order_payment = OrderPayment.objects.create(order=cls.order, customer=cls.customer, date=cls.date, type=OrderPayment.PAYMENT_CHOICES, total=cls.order.total, notes='test order payment')
        cls.empty_data = {'order': '', 'customer': '', 'date': '', 'type': '', 'total': '', 'notes': ''}
        cls.long_data = {'order': cls.order.pk, 'customer': cls.customer.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CASH, 'total': cls.order.total, 'notes': cls.long_string}
        cls.negative_data = {'order': cls.order.pk, 'customer': cls.customer.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CASH, 'total': -65.38, 'notes': 'test notes'}
        cls.create_data = {'order': cls.order.pk, 'customer': cls.customer.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CASH, 'total': cls.order.total, 'notes': 'test notes'}
        cls.update_data = {'order': cls.order.pk, 'customer': cls.customer.pk, 'date': cls.date, 'type': OrderPayment.PAYMENT_CHOICES.CHECK, 'total': cls.order.total, 'notes': 'updated test notes'}
        cls.patch_data = {'notes': 'updated test order payment notes'}
        # cls.create_url = reverse('order-payment-create')
        # cls.list_url = lambda pk: reverse('order-payment-list', kwargs={'pk': pk, 'type': 'm'})
        # cls.detail_url = lambda pk: reverse('order-payment-detail', kwargs={'pk': pk, 'type':'s'})
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))
        
    ## Test get order payment not found
    def test_get_order_payment_not_found(self):
        pass

    ## Test get order payment success
    def test_get_order_payment_success(self):
        pass

    ## Test get order payments success
    def test_get_order_payments_success(self):
        pass

    ## Test create order payment with empty data
    def test_create_order_payment_empty_data(self):
        pass

    ## Test create order payment with long data
    def test_create_order_payment_long_data(self):
        pass

    ## Test create order payment with negative data
    def test_create_order_payment_negative_data(self):
        pass

    ## Test create order payment success
    def test_create_order_payment_success(self):
        pass

    ## Test update order payment with empty data
    def test_update_order_payment_empty_data(self):
        pass

    ## Test update order payment with long data
    def test_update_order_payment_long_data(self):
        pass

    ## Test update order payment with negative data
    def test_update_order_payment_negative_data(self):
        pass

    ## Test update order payment success
    def test_update_order_payment_success(self):
        pass

    ## Test partial update order payment with empty data
    def test_partial_update_order_payment_empty_data(self):
        pass

    ## Test partial update order payment with long data
    def test_partial_update_order_payment_long_data(self):
        pass

    ## Test partial update order payment with negative data
    def test_partial_update_order_payment_negative_data(self):
        pass

    ## Test partial update order payment success
    def test_partial_update_order_payment_success(self):
        pass

    ## Test delete order payment success
    def test_delete_order_payment_success(self):
        pass
