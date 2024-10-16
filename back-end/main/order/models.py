from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.db import models, transaction
from asset.models import AssetInstance
from customer.models import Customer
from material.models import Material
from service.models import Service
from user.models import User
from tool.models import Tool
from django.db import models
from decimal import Decimal

# Order model
class Order(models.Model):
    class CALLOUT_CHOICES(models.TextChoices):
        STANDARD = '50.0', 'Standard - $50.00'
        EMERGENCY = '175.0', 'Emergency - $175.00'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=2000, validators=[MinLengthValidator(2), MaxLengthValidator(2000)])
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=93.0, validators=[MinValueValidator(Decimal(75.0))])
    hours_worked = models.DecimalField(max_digits=10, decimal_places=2, default=3.0, validators=[MinValueValidator(Decimal(3.0))])
    labor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    material_upcharge = models.DecimalField(max_digits=10, decimal_places=2, default=25.0, validators=[MinValueValidator(Decimal(15.0)), MaxValueValidator(Decimal(75.0))])
    material_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    asset_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    line_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=12.0, validators=[MinValueValidator(Decimal(0.0)), MaxValueValidator(Decimal(20.0))])
    tax_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    completed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0)), MaxValueValidator(Decimal(100.0))])
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    payment_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    working_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    notes = models.CharField(max_length=10000, validators=[MaxLengthValidator(10000)], null=True, blank=True)
    callout = models.FloatField(choices=CALLOUT_CHOICES.choices, default=CALLOUT_CHOICES.STANDARD)

    def calculate_hours_worked(self):
        work_logs = OrderWorkLog.objects.filter(order=self)
        total_hours = sum((log.end - log.start).total_seconds() / 3600 for log in work_logs)
        return max(float(total_hours), 3.0)

    def calculate_labor_total(self):
        return max(float(self.hourly_rate) * float(self.hours_worked), 0.0)

    def calculate_material_total(self):
        materials = OrderMaterial.objects.filter(order__pk=self.pk)
        total_material_costs = sum((material.material.unit_cost * material.quantity) for material in materials)
        return max(float(total_material_costs) * (1 + float(self.material_upcharge) / 100), 0.0)

    def calculate_asset_total(self):
        assets = OrderAsset.objects.filter(order__pk=self.pk)
        total_asset_costs = sum((asset.instance.rental_cost * asset.usage) for asset in assets)
        return max(float(total_asset_costs), 0.0)

    def calculate_line_total(self):
        costs = OrderCost.objects.filter(order__pk=self.pk)
        return max(float(sum(cost.cost for cost in costs)), 0.0)

    def calculate_subtotal(self):
        return max(float(self.labor_total) + float(self.material_total) + float(self.asset_total) + float(self.line_total) + float(self.callout), 0)

    def calculate_tax_total(self):
        return max((float(self.tax) / 100) * float(self.subtotal), 0.0)

    def calculate_discount_total(self):
        return max((float(self.discount) / 100) * float(self.subtotal), 0.0)

    def calculate_total(self):
        return max(float(self.subtotal) + float(self.tax_total) - float(self.discount_total), 0.0)

    def calculate_payment_total(self):
        return max(float(sum(payment.total for payment in OrderPayment.objects.filter(order=self))), 0.0)

    def calculate_working_total(self):
        return max(float(self.total) - float(self.payment_total), 0.0)

    def determine_paid(self):
        if self.working_total == 0:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.hours_worked = round(self.calculate_hours_worked(), 2)
        self.labor_total = round(self.calculate_labor_total(), 2)
        self.material_total = round(self.calculate_material_total(), 2)
        self.asset_total = round(self.calculate_asset_total(), 2)
        self.line_total = round(self.calculate_line_total(), 2)
        self.subtotal = round(self.calculate_subtotal(), 2)
        self.tax_total = round(self.calculate_tax_total(), 2)
        self.discount_total = round(self.calculate_discount_total(), 2)
        self.total = round(self.calculate_total(), 2)
        self.payment_total = round(self.calculate_payment_total(), 2)
        self.working_total = round(self.calculate_working_total(), 2)
        self.paid = self.determine_paid()
        super().save()

# Order work log model
class OrderWorkLog(models.Model):
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
        # Recalculate the order fields after saving the work log
        self.order.save()

# Order cost model
class OrderCost(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='costs')
    name = models.CharField(max_length=300, validators=[MinLengthValidator(2), MaxLengthValidator(300)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Recalculate the order fields after saving a cost
        self.order.save()

# Order picture model
class OrderPicture(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='orders')

# Order material model
class OrderMaterial(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.quantity > 0:
                # Update material's available quantity and unit cost
                self.material.available_quantity -= self.quantity
                self.material.save()
            super().save(*args, **kwargs)
            # Update the purchase total
            self.order.save()

    def delete(self, *args, **kwargs):
        self.material.available_quantity += self.quantity
        self.material.save()
        super().delete(*args, **kwargs)
        # Update the order total after deletion
        self.order.save()

# Order tool model
class OrderTool(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tools')
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    quantity_used = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    quantity_broken = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.quantity_broken > 0:
                # Update tool's available quantity and unit cost
                self.tool.available_quantity -= self.quantity_broken
            self.tool.save()
            super().save(*args, **kwargs)
            # Update the purchase total
            self.order.save()

    def delete(self, *args, **kwargs):
        self.tool.available_quantity += self.quantity_broken
        self.tool.save()
        super().delete(*args, **kwargs)
        # Update the order total after deletion
        self.order.save()

# Order asset model
class OrderAsset(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='assets')
    instance = models.ForeignKey(AssetInstance, on_delete=models.CASCADE)
    usage = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0.0))])
    condition = models.CharField(max_length=21, choices=AssetInstance.CONDITION_CHOICES, default=AssetInstance.CONDITION_CHOICES.GOOD, validators=[MaxLengthValidator(17)])

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.instance.usage += self.usage
            self.instance.condition = self.condition
            self.instance.save()
            super().save(*args, **kwargs)
            # Update the purchase total
            self.order.save()

    def delete(self, *args, **kwargs):
        self.instance.usage -= self.usage
        self.instance.save()
        super().delete(*args, **kwargs)
        # Update the order total after deletion
        self.order.save()

# Order payment model
class OrderPayment(models.Model):
    class PAYMENT_CHOICES(models.TextChoices):
        CASH = 'cash', 'Cash'
        CHECK = 'check', 'Check'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    date = models.DateField()
    type = models.CharField(max_length=5, choices=PAYMENT_CHOICES.choices)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    notes = models.CharField(max_length=255, validators=[MaxLengthValidator(255)], blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Recalculate the order fields after saving a payment
        self.order.save()

# Order Worker model
class OrderWorker(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='workers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])

    def save(self, *args, **kwargs):
        self.total = self.user.pay_rate * self.order.hours_worked
        super().save(*args, **kwargs)
