from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from customer.models import Customer
from material.models import Material
from service.models import Service
from django.db import models

# Order model
class Order(models.Model):
    class CALLOUT_CHOICES(models.TextChoices):
        STANDARD = 50.0, 'Standard - $50.00'
        EMERGENCY = 175.0, 'Emergency - $175.00'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=2000, validators=[MinLengthValidator(2), MaxLengthValidator(2000)])
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    hourly_rate = models.FloatField(default=93.0, validators=[MinValueValidator(75.0)])
    hours_worked = models.FloatField(default=3.0, validators=[MinValueValidator(3.0)])
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
        materials = OrderMaterial.objects.filter(order=self)
        total_material_costs = sum(material.price for material in materials)
        material_costs = total_material_costs * (1 + self.material_upcharge / 100)
        # Calculate order costs
        costs = OrderCost.objects.filter(order=self)
        order_costs = sum(cost.cost for cost in costs)
        subtotal = labor_costs + material_costs + order_costs + float(self.callout)
        tax_amount = (self.tax / 100) * subtotal
        discount_amount = (self.discount / 100) * subtotal
        total = subtotal + tax_amount - discount_amount
        return max(total, 0)
    
    def save(self, *args, **kwargs):
        # Automatically calculate total
        self.total = self.calculate_total()
        super().save(*args, **kwargs)

# Order cost model
class OrderCost(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='costs')
    name = models.CharField(max_length=300, validators=[MinLengthValidator(2), MaxLengthValidator(300)])
    cost = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])

# Order picture model
class OrderPicture(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to='media/orders')

# Order material model
class OrderMaterial(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])

    def save(self, *args, **kwargs):
        self.price = self.material.unit_cost * self.quantity
        super().save(*args, **kwargs)

# Order payment model
class OrderPayment(models.Model):
    class PAYMENT_CHOICES(models.TextChoices):
        CASH = 'cash', 'Cash'
        CHECK = 'check', 'Check'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    date = models.DateField()
    type = models.CharField(max_length=5, choices=PAYMENT_CHOICES.choices)
    total = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    notes = models.CharField(max_length=255, validators=[MaxLengthValidator(255)], blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        order = self.order
        total_payments = sum(payment.total for payment in OrderPayment.objects.filter(order=order))
        if total_payments >= order.total:
            order.paid = True
            order.save()
