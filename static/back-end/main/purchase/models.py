from supplier.models import Supplier, SupplierAddress
from django.core.validators import MinValueValidator
from django.db import models

# Purchase model
class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supplier_address = models.ForeignKey(SupplierAddress, on_delete=models.CASCADE)
    tax = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    total = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    date = models.DateField()
    reciept = models.ImageField(upload_to='media/purchases/')

    def __str__(self):
        return f'OHMS{self.pk}-PUR'
    