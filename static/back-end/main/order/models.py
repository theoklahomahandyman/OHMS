from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from customer.models import Customer
from material.models import Material
from service.models import Service
from django.db import models

# Order model
class Order(models.Model):
    class CALLOUTCHOICES(models.TextChoices):
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
    paid = models.BooleanField(defualt=False)
    discount = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    notes = models.CharField(max_length=10000, validators=[MaxLengthValidator(10000)], null=True, blank=True)
    callout = models.FloatField(choices=CALLOUTCHOICES, default=CALLOUTCHOICES.STANDARD)

class OrderCost(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, validators=[MinLengthValidator(2), MaxLengthValidator(300)])
    cost = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])

class OrderPicture(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/orders')

# order_material model with many to many relationship to allow multiple materials to an order
# order_payment model with many to many relationship to allow multiple payments to an order