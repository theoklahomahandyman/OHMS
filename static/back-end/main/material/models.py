from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.db import models

# Material model
class Material(models.Model):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    description = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])
    size = models.CharField(max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    unit_cost = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    available_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'size'], name='unique_material')
        ]

    def __str__(self):
        return f'OHMS{self.pk}-MAT'
