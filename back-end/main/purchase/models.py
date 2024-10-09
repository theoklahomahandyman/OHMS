from supplier.models import Supplier, SupplierAddress
from django.core.validators import MinValueValidator
from django.db import models, transaction
from material.models import Material
from django.db.models import Sum
from tool.models import Tool
from decimal import Decimal

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supplier_address = models.ForeignKey(SupplierAddress, on_delete=models.CASCADE)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    material_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    tool_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    date = models.DateField()

    def calculate_material_total(self):
        materials = PurchaseMaterial.objects.filter(purchase__pk=self.pk)
        total_material_costs = sum(material.cost for material in materials)
        return max(float(total_material_costs), 0.0)

    def calculate_tool_total(self):
        tools = PurchaseTool.objects.filter(purchase__pk=self.pk)
        total_tool_costs = sum(tool.cost for tool in tools)
        return max(float(total_tool_costs), 0.0)

    def calculate_total(self):
        return max(float(self.material_total) + float(self.tool_total) + float(self.tax), 0.0)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Set initial total to tax if no PK exists (new instance)
            if not self.pk:
                self.total = self.tax
            super().save(*args, **kwargs)
        self.material_total = round(self.calculate_material_total(), 2)
        self.tool_total = round(self.calculate_tool_total(), 2)
        self.total = round(self.calculate_total(), 2)
        super().save()

# Purchase reciept model
class PurchaseReciept(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='purchases')

class PurchaseMaterial(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0.0))])

    def calculate_unit_cost(self):
        unit_cost = float(self.cost) / float(self.quantity)
        return max(unit_cost, 0.0)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.quantity > 0:
                # Update material's available quantity and unit cost
                self.material.available_quantity += self.quantity
                self.material.unit_cost = self.calculate_unit_cost()
            else:
                # Handle zero quantity (don't update available quantity)
                self.material.unit_cost = 0.0
            self.material.save()
            super().save(*args, **kwargs)
            # Update the purchase total
            self.purchase.save()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Subtract cost from purchase total before deletion
            self.material.available_quantity -= self.quantity
            self.material.save()
            self.purchase.total -= self.cost
            self.purchase.save()
            super().delete(*args, **kwargs)

class PurchaseTool(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='tools')
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0.0))])

    def calculate_unit_cost(self):
        unit_cost = float(self.cost) / float(self.quantity)
        return max(unit_cost, 0.0)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.quantity > 0:
                # Update tool's available quantity and unit cost
                self.tool.available_quantity += self.quantity
                self.tool.unit_cost = self.calculate_unit_cost()
            else:
                # Handle zero quantity (don't update available quantity)
                self.tool.unit_cost = 0.0
            self.tool.save()
            super().save(*args, **kwargs)
            # Update the purchase total
            self.purchase.save()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Subtract cost from purchase total before deletion
            self.tool.available_quantity -= self.quantity
            self.tool.save()
            self.purchase.total -= self.cost
            self.purchase.save()
            super().delete(*args, **kwargs)
