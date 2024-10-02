from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from customer.models import Customer
from material.models import Material
from service.models import Service
from django.db import models

# Order model
class Order(models.Model):
    class CALLOUT_CHOICES(models.TextChoices):
        STANDARD = '50.0', 'Standard - $50.00'
        EMERGENCY = '175.0', 'Emergency - $175.00'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=2000, validators=[MinLengthValidator(2), MaxLengthValidator(2000)])
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    hourly_rate = models.FloatField(default=93.0, validators=[MinValueValidator(75.0)])
    hours_worked = models.FloatField(default=3.0, validators=[MinValueValidator(3.0)])
    """
        labor_total
        material_total
        line_total
        tax_total
        discount_total
        payment_total
        working_total
    """
    material_upcharge = models.FloatField(default=25.0, validators=[MinValueValidator(15.0), MaxValueValidator(75.0)])
    tax = models.FloatField(default=12.0, validators=[MinValueValidator(0.0), MaxValueValidator(20.0)])
    total = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    completed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    discount = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    notes = models.CharField(max_length=10000, validators=[MaxLengthValidator(10000)], null=True, blank=True)
    callout = models.FloatField(choices=CALLOUT_CHOICES.choices, default=CALLOUT_CHOICES.STANDARD)

    def calculate_total(self):
        # Calculate labor costs
        labor_costs = self.hourly_rate * self.hours_worked
        # Calculate material costs
        materials = OrderMaterial.objects.filter(order__pk=self.pk)
        total_material_costs = sum((material.material.unit_cost * material.quantity) for material in materials)
        material_costs = total_material_costs * (1 + self.material_upcharge / 100)
        # Calculate order costs
        costs = OrderCost.objects.filter(order__pk=self.pk)
        order_costs = sum(cost.cost for cost in costs)
        subtotal = labor_costs + material_costs + order_costs + float(self.callout)
        tax_amount = (self.tax / 100) * subtotal
        discount_amount = (self.discount / 100) * subtotal
        total = subtotal + tax_amount - discount_amount
        return max(total, 0)

    def calculate_hours_worked(self):
        work_logs = OrderWorkLog.objects.filter(order=self)
        total_hours = sum((log.end - log.start).total_seconds() / 3600 for log in work_logs)
        return max(total_hours, 3.0)

    def determine_paid(self):
        total_payments = sum(payment.total for payment in OrderPayment.objects.filter(order=self))
        if total_payments >= self.total:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.hours_worked = self.calculate_hours_worked()
        self.total = self.calculate_total()

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
        # Recalculate the hours worked and order total after saving the work log
        self.order.hours_worked = self.order.calculate_hours_worked()
        self.order.total = self.order.calculate_total()
        # Redetermine paid after saving the work log
        self.order.paid = self.order.determine_paid()
        self.order.save()

# Order cost model
class OrderCost(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='costs')
    name = models.CharField(max_length=300, validators=[MinLengthValidator(2), MaxLengthValidator(300)])
    cost = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Recalculate the order total and redetermine paid after saving a cost
        self.order.total = self.order.calculate_total()
        self.order.paid = self.order.determine_paid()
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
        super().save(*args, **kwargs)
        # Recalculate the order total and redetermine paid after saving a material
        self.order.total = self.order.calculate_total()
        self.order.paid = self.order.determine_paid()
        self.order.save()

# Order payment model
class OrderPayment(models.Model):
    class PAYMENT_CHOICES(models.TextChoices):
        CASH = 'cash', 'Cash'
        CHECK = 'check', 'Check'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    date = models.DateField()
    type = models.CharField(max_length=5, choices=PAYMENT_CHOICES.choices)
    total = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    notes = models.CharField(max_length=255, validators=[MaxLengthValidator(255)], blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.paid = self.order.determine_paid()
        self.order.save()
