from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal

# User model
class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100, validators=[MinLengthValidator(2), MaxLengthValidator(100)])
    last_name = models.CharField(max_length=100, validators=[MinLengthValidator(2), MaxLengthValidator(100)])
    email = models.EmailField(unique=True, max_length=255, validators=[MinLengthValidator(8), MaxLengthValidator(255)])
    phone = models.CharField(max_length=17, validators=[MinLengthValidator(16), MaxLengthValidator(17)])
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
