from supplier.models import Supplier, SupplierAddress
from django.core.validators import MinValueValidator
from material.models import Material
from django.db import models

# Purchase model
class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supplier_address = models.ForeignKey(SupplierAddress, on_delete=models.CASCADE)
    tax = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    total = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    date = models.DateField()
    reciept = models.ImageField(upload_to='media/purchases/')

    def save(self, *args, **kwargs):
        # Save first to ensure instance has a primary key for searching for purchase materials
        if not self.pk:
            self.total = self.tax        
        super().save(*args, **kwargs)

    def __str__(self):
        return f'OHMS{self.pk}-PUR'
    
# Material purchase model
class PurchaseMaterial(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    cost = models.FloatField(validators=[MinValueValidator(0.0)])

    def save(self, *args, **kwargs):
        # Calculate new unit cost, switch from average to replace with new cost

        ## Average method
        # previous_total_cost = (self.material.unit_cost * self.material.available_quantity)
        # new_total_cost = previous_total_cost + self.cost
        # new_total_quantity = self.material.available_quantity + self.quantity
        # if new_total_quantity > 0:
        #     new_unit_cost = new_total_cost / new_total_quantity
        # else:
        #     new_unit_cost = 0.0

        ## Replacment method
        if self.quantity > 0:
            new_unit_cost = self.cost / self.quantity
        else:
            new_unit_cost = 0.0

        # Update material unit cost
        self.material.unit_cost = new_unit_cost
        self.material.available_quantity += self.quantity
        self.material.save()

        # Update purchase total
        purchase_materials = PurchaseMaterial.objects.filter(purchase=self.purchase)
        total_costs = self.purchase.tax + self.cost + sum(purchase_material.cost for purchase_material in purchase_materials)
        self.purchase.total = total_costs
        self.purchase.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.material.name} - {self.quantity} units purchased for ${self.cost}'
