from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from utils.fields import PresignedURLImageField
from utils.mixins import AtomicOperationsMixin
from inventory.models import Material, Tool
from customer.models import Customer
from service.models import Service
from user.models import User
from django.db import models
from decimal import Decimal

''' Model for orders '''
class Order(models.Model):
    class CALLOUT_CHOICES(AtomicOperationsMixin, models.TextChoices):
        STANDARD = '50.0', 'Standard - $50.00'
        EMERGENCY = '175.0', 'Emergency - $175.00'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=2000, validators=[MinLengthValidator(2), MaxLengthValidator(2000)])
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=93.0, validators=[MinValueValidator(Decimal(75.0))])
    material_upcharge = models.DecimalField(max_digits=10, decimal_places=2, default=25.0, validators=[MinValueValidator(Decimal(15.0)), MaxValueValidator(Decimal(75.0))])
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=12.0, validators=[MinValueValidator(Decimal(0.0)), MaxValueValidator(Decimal(20.0))])
    completed = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0)), MaxValueValidator(Decimal(100.0))])
    notes = models.CharField(max_length=10000, validators=[MaxLengthValidator(10000)], null=True, blank=True)
    callout = models.FloatField(choices=CALLOUT_CHOICES.choices, default=CALLOUT_CHOICES.STANDARD)

    ''' Dynamically calculate order hours worked '''
    @property
    def hours_worked(self):
        work_logs = OrderWorkLog.objects.filter(order=self)
        total_hours = sum((log.end - log.start).total_seconds() / 3600 for log in work_logs)
        return Decimal(max(float(total_hours), 3.0))

    ''' Dynamically calculate order labor total '''
    @property
    def labor_total(self):
        return Decimal(max(float(self.hourly_rate) * float(self.hours_worked), 0.0))

    ''' Dynamically calculate the order material total based '''
    @property
    def material_total(self):
        materials = OrderMaterial.objects.filter(order__pk=self.pk)
        total_material_costs = sum((material.inventory_item.unit_cost * material.quantity) for material in materials)
        return Decimal(max(float(total_material_costs) * (1 + float(self.material_upcharge) / 100), 0.0))

    ''' Dynamically calculate the order asset total '''
    # @property
    # def asset_total(self):
    #     assets = OrderAsset.objects.filter(order__pk=self.pk)
    #     total_asset_costs = sum((asset.instance.rental_cost * asset.usage) for asset in assets)
    #     return Decimal(max(float(total_asset_costs), 0.0)).quantize(Decimal('0.01'))

    ''' Dynamically calculate the order line item total '''
    @property
    def line_total(self):
        costs = OrderCost.objects.filter(order__pk=self.pk)
        return max(Decimal(sum(cost.cost for cost in costs)), Decimal(0.0))

    ''' Dynamically calculate the order subtotal '''
    @property
    def subtotal(self):
        return Decimal(max(float(self.labor_total) + float(self.material_total) + float(self.line_total) + float(self.callout), 0))

    ''' Dynamically calculate the order tax total '''
    @property
    def tax_total(self):
        return Decimal(max((float(self.tax) / 100) * float(self.subtotal), 0.0))

    ''' Dynamically calculate the order discount total '''
    @property
    def discount_total(self):
        return Decimal(max((float(self.discount) / 100) * float(self.subtotal), 0.0))

    ''' Dynamically calculate the order total '''
    @property
    def total(self):
        return Decimal(max(float(self.subtotal) + float(self.tax_total) - float(self.discount_total), 0.0))

    ''' Dynamically calculate the total from payments on an order '''
    @property
    def payment_total(self):
        return Decimal(max(float(sum(payment.total for payment in OrderPayment.objects.filter(order=self))), 0.0))

    ''' Dynamically calculate the order working total or total due '''
    @property
    def working_total(self):
        return Decimal(max(float(self.total) - float(self.payment_total), 0.0))

    ''' Dynamically calculate if the order is paid '''
    @property
    def paid(self):
        if self.working_total == 0:
            return True
        else:
            return False

''' Model for order work logs '''
class OrderWorkLog(AtomicOperationsMixin, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='work_logs')
    start = models.DateTimeField()
    end = models.DateTimeField()

    def clean(self):
        # Ensure the end time is after the start time
        if self.end <= self.start:
            raise ValidationError('The start time must be before the end time.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

''' Model for order line item charges '''
class OrderCost(AtomicOperationsMixin, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='costs')
    name = models.CharField(max_length=300, validators=[MinLengthValidator(2), MaxLengthValidator(300)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])

'''
    Model for order pictures
    ---------------------------
    Note: Ensure the 'Pillow' library is installed to handle image storage and manipulation.
'''
class OrderPicture(AtomicOperationsMixin, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='images')
    image = PresignedURLImageField(upload_to='orders', null=True, blank=True)

''' Abstract base model for order inventory items with shared fields and overrides '''
class OrderInventory(AtomicOperationsMixin, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    # Ensures model is abstract and not created in database
    class Meta:
        abstract = True

    ''' Overrides save method to ensure inventory is refreshed '''
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if hasattr(self.inventory_item, 'items_used'):
            self.inventory_item.items_used.add(self)
        elif hasattr(self.inventory_item, 'items_broken'):
            self.inventory_item.items_broken.add(self)
        self.inventory_item.refresh_from_db()

    ''' Overrides save method to ensure inventory is refreshed '''
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if hasattr(self.inventory_item, 'items_used'):
            self.inventory_item.items_used.remove(self)
        elif hasattr(self.inventory_item, 'items_broken'):
            self.inventory_item.items_broken.remove(self)
        self.inventory_item.refresh_from_db()

''' Model for materials used in an order '''
class OrderMaterial(OrderInventory):
    inventory_item = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='order_materials')
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0.0))], default=0.0)

    '''
        Override save method to auto calculate cost
        Calculate cost based on the unit_cost and quantity
    '''
    def save(self, *args, **kwargs):
        # Only calculate if cost is not set or is 0
        if not self.cost or self.cost == Decimal('0.0'):
            self.cost = Decimal(float(self.inventory_item.unit_cost) * float(self.quantity)).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)

''' Model for tools used and broken in an order '''
class OrderTool(OrderInventory):
    inventory_item = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='order_tools')
    quantity_broken = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

''' Model for assets used in an order '''
# class OrderAsset(AtomicOperationsMixin, models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='assets')
#     instance = models.ForeignKey(AssetInstance, on_delete=models.CASCADE)
#     usage = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0.0))])
#     condition = models.CharField(max_length=21, choices=AssetInstance.CONDITION_CHOICES, default=AssetInstance.CONDITION_CHOICES.GOOD, validators=[MaxLengthValidator(17)])

#     def save(self, *args, **kwargs):
#         with transaction.atomic():
#             self.instance.usage += self.usage
#             self.instance.condition = self.condition
#             self.instance.save()
#             super().save(*args, **kwargs)
#             # Update the purchase total
#             self.order.save()

#     def delete(self, *args, **kwargs):
#         self.instance.usage -= self.usage
#         self.instance.save()
#         super().delete(*args, **kwargs)
#         # Update the order total after deletion
#         self.order.save()

''' Model for payments made to an order '''
class OrderPayment(AtomicOperationsMixin, models.Model):
    class PAYMENT_CHOICES(models.TextChoices):
        CASH = 'cash', 'Cash'
        CHECK = 'check', 'Check'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    date = models.DateField()
    type = models.CharField(max_length=5, choices=PAYMENT_CHOICES.choices)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    notes = models.CharField(max_length=255, validators=[MaxLengthValidator(255)], blank=True, null=True)

''' Model for workers involved in an order '''
class OrderWorker(AtomicOperationsMixin, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='workers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])

    def save(self, *args, **kwargs):
        self.total = Decimal(float(self.user.pay_rate) * float(self.order.hours_worked)).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
