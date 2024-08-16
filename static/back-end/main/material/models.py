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

# # Material purchase model
# class PurchaseMaterial(models.Model):
#     purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
#     material = models.ForeignKey(Material, on_delete=models.CASCADE)
#     purchase_quantity = models.PositiveIntegerField()
#     purchase_cost = models.FloatField(validators=[MinValueValidator(0.0)])

#     def save(self, *args, **kwargs):
#         # Calculate new average unit cost, switch from average to replace with new cost
#         previous_total_cost = (self.material.unit_cost * self.material.available_quantity)
#         new_total_cost = previous_total_cost + self.purchase_cost
#         new_total_quantity = self.material.available_quantity + self.purchase_quantity
#         if new_total_quantity > 0:
#             new_unit_cost = new_total_cost / new_total_quantity
#         else:
#             new_unit_cost = 0.0
#         # Update material unit cost
#         self.material.unit_cost = new_unit_cost
#         self.material.available_quantity = new_total_quantity
#         self.material.save()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f'{self.material.name} - {self.purchase_quantity} units purchased for ${self.purchase_cost}'
