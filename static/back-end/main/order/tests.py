from order.serializers import OrderSerializer, OrderCostSerializer, OrderPictureSerializer, OrderMaterialSerializer, OrderPaymentSerializer
from order.models import Order, OrderCost, OrderPicture, OrderMaterial, OrderPayment
from django.core.files.uploadedfile import SimpleUploadedFile
from customer.models import Customer
from material.models import Material
from service.models import Service
from django.utils import timezone
from django.test import TestCase

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

    # Test order model save method and the use of the calculate_total method
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

    # Test order material model save method
    def test_order_material_save(self):
        order_material = OrderMaterial(order=self.order, material=self.material, quantity=5)
        order_material.save()
        expected_price = self.material.unit_cost * order_material.quantity
        order_material.refresh_from_db()
        self.assertAlmostEqual(order_material.price, expected_price, places=2)

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

    # Test order serializer with empty data
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

    # Test order serializer with short data
    def test_order_serializer_short_data(self):
        serializer = OrderSerializer(data=self.short_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)
        self.assertIn('hourly_rate', serializer.errors)
        self.assertIn('hours_worked', serializer.errors)
        self.assertIn('material_upcharge', serializer.errors)

    # Test order serializer with long data
    def test_order_serializer_long_data(self):
        serializer = OrderSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)
        self.assertIn('material_upcharge', serializer.errors)
        self.assertIn('tax', serializer.errors)
        self.assertIn('discount', serializer.errors)

    # Test order serializer with negative data
    def test_order_serializer_negative_data(self):
        serializer = OrderSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('hourly_rate', serializer.errors)
        self.assertIn('hours_worked', serializer.errors)
        self.assertIn('material_upcharge', serializer.errors)
        self.assertIn('tax', serializer.errors)
        self.assertIn('total', serializer.errors)
        self.assertIn('discount', serializer.errors)

    # Test order serializer validation success
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

    # Test order cost serializer with empty data
    def test_order_cost_serializer_empty_data(self):
        serializer = OrderCostSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)
        self.assertIn('name', serializer.errors)
        self.assertIn('cost', serializer.errors)

    # Test order cost serializer with short data
    def test_order_cost_serializer_short_data(self):
        serializer = OrderCostSerializer(data=self.short_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    # Test order cost serializer with long data
    def test_order_cost_serializer_long_data(self):
        serializer = OrderCostSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    # Test order cost serializer with negative data
    def test_order_cost_serializer_negative_data(self):
        serializer = OrderCostSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('cost', serializer.errors)

    # Test order cost serializer validation success
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

    # Test order picture serializer with empty data
    def test_order_picture_serializer_empty_data(self):
        serializer = OrderPictureSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)
        self.assertIn('image', serializer.errors)

    # Test order picture serializer validation success
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

    # Test order material serializer with empty data
    def test_order_material_serializer_empty_data(self):
        serializer = OrderMaterialSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)
        self.assertIn('material', serializer.errors)
        self.assertIn('quantity', serializer.errors)
        self.assertIn('price', serializer.errors)

    # Test order material serializer with negative data
    def test_order_material_serializer_negative_data(self):
        serializer = OrderMaterialSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)
        self.assertIn('price', serializer.errors)

    # Test order material serializer validation success
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

    # Test order payment serializer with empty data
    def test_order_payment_serializer_empty_data(self):
        serializer = OrderPaymentSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('order', serializer.errors)
        self.assertIn('customer', serializer.errors)
        self.assertIn('date', serializer.errors)
        self.assertIn('type', serializer.errors)
        self.assertIn('total', serializer.errors)

    # Test order payment serializer with long data
    def test_order_payment_serializer_long_data(self):
        serializer = OrderPaymentSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('notes', serializer.errors)

    # Test order payment serializer with negative data
    def test_order_payment_serializer_negative_data(self):
        serializer = OrderPaymentSerializer(data=self.negative_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('total', serializer.errors)

    # Test order payment serializer validation success
    def test_order_payment_serializer_validation_success(self):
        serializer = OrderPaymentSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('order', serializer.validated_data)
        self.assertIn('customer', serializer.validated_data)
        self.assertIn('date', serializer.validated_data)
        self.assertIn('type', serializer.validated_data)
        self.assertIn('total', serializer.validated_data)
        self.assertIn('notes', serializer.validated_data)
