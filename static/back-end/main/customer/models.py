from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

# Customer model
class Customer(models.Model):
    first_name = models.CharField(max_length=100, validators=[MinLengthValidator(2), MaxLengthValidator(100)])
    last_name = models.CharField(max_length=100, validators=[MinLengthValidator(2), MaxLengthValidator(100)])
    email = models.EmailField(unique=True, max_length=255, validators=[MinLengthValidator(8), MaxLengthValidator(255)])
    phone = models.CharField(max_length=17, validators=[MinLengthValidator(16), MaxLengthValidator(17)])
    notes = models.CharField(blank=True, null=True, max_length=600, validators=[MaxLengthValidator(600)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
