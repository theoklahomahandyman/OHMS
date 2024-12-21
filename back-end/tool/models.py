from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
from decimal import Decimal

# Tool model
class Tool(models.Model):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    description = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    available_quantity = models.PositiveIntegerField(default=0)
