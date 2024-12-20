from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
from decimal import Decimal

# Material model
class Material(models.Model):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    description = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])
    size = models.CharField(max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    available_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'size'], name='unique_material')
        ]
