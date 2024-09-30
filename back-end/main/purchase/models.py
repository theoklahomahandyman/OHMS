from supplier.models import Supplier, SupplierAddress
from django.core.validators import MinValueValidator
from django.db import models, transaction
from material.models import Material

# Purchase model
class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supplier_address = models.ForeignKey(SupplierAddress, on_delete=models.CASCADE)
    tax = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    total = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    date = models.DateField()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Save first to ensure instance has a primary key for searching for purchase materials
            if not self.pk:
                self.total = self.tax
            super().save(*args, **kwargs)

    def __str__(self):
        return f'OHMS{self.pk}-PUR'

# Purchase reciept model
class PurchaseReciept(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='reciepts')
    image = models.ImageField(upload_to='purchases')

# Purchase material model
class PurchaseMaterial(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    cost = models.FloatField(validators=[MinValueValidator(0.0)])

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Calculate new unit cost with replacement
            if self.quantity > 0:
                new_unit_cost = self.cost / self.quantity
            else:
                new_unit_cost = 0.0

            # Update material unit cost
            self.material.unit_cost = new_unit_cost
            self.material.available_quantity += self.quantity
            self.material.save()

            # Handle purchase total updates
            if self.pk:
                original = PurchaseMaterial.objects.get(pk=self.pk)
                self.purchase.total += self.cost - original.cost
            else:
                self.purchase.total += self.cost
            self.purchase.save()

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Subtract cost from purchase total before deletion
            self.purchase.total -= self.cost
            self.purchase.save()
            super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.material.name} - {self.quantity} units purchased for ${self.cost}'
