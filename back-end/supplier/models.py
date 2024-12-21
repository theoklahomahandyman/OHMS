from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

# Supplier model
class Supplier(models.Model):
    name = models.CharField(unique=True, max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    notes = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])

    def __str__(self):
        return self.name

class SupplierAddress(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    city = models.CharField(max_length=100, validators=[MinLengthValidator(2), MaxLengthValidator(100)])
    state = models.CharField(max_length=13, validators=[MinLengthValidator(2), MaxLengthValidator(13)])
    zip = models.PositiveIntegerField()
    notes = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])

    def __str__(self):
        return f'{self.street_address} {self.city}, {self.state} {self.zip}'
