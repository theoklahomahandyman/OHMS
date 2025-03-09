from supplier.models import Supplier, SupplierAddress
from django.core.validators import MinValueValidator
from utils.fields import PresignedURLImageField
from utils.mixins import AtomicOperationsMixin
from inventory.models import Material, Tool
from django.db import models
from decimal import Decimal

''' Model for purchases '''
class Purchase(AtomicOperationsMixin, models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supplier_address = models.ForeignKey(SupplierAddress, on_delete=models.CASCADE)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    date = models.DateField()

    ''' Dynamically calculate purchase material total '''
    @property
    def material_total(self):
        materials = PurchaseMaterial.objects.filter(purchase__pk=self.pk)
        total_material_costs = sum(material.cost for material in materials)
        return Decimal(max(float(total_material_costs), 0.0)).quantize(Decimal('0.01'))

    ''' Dynamically calculate purchase tool total '''
    @property
    def tool_total(self):
        tools = PurchaseTool.objects.filter(purchase__pk=self.pk)
        total_tool_costs = sum(tool.cost for tool in tools)
        return Decimal(max(float(total_tool_costs), 0.0)).quantize(Decimal('0.01'))

    ''' Dynamically calculate purchase asset total '''
    # @property
    # def asset_total(self):
    #     assets = PurchaseAsset.objects.filter(purchase__pk=self.pk)
    #     total_asset_costs = sum(asset.cost for asset in assets)
    #     return Decimal(max(float(total_asset_costs), 0.0)).quantize(Decimal('0.01'))

    ''' Dynamically calculate purchase subtotal '''
    @property
    def subtotal(self):
        return Decimal(max(float(self.material_total) + float(self.tool_total), 0.0)).quantize(Decimal('0.01'))

    ''' Dynamically calculate purchase total '''
    @property
    def total(self):
        return Decimal(max(float(self.subtotal) + float(self.tax), 0.0)).quantize(Decimal('0.01'))

'''
    Model for purchase in a purchase
    ---------------------------
    Note: Ensure the 'Pillow' library is installed to handle image storage and manipulation.
'''
class PurchaseReceipt(AtomicOperationsMixin, models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='images')
    image = PresignedURLImageField(folder_name='purchases', null=True, blank=True)

''' Abstract base model for purchase inventory items with shared fields and overrides '''
class PurchaseInventory(AtomicOperationsMixin, models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0.0))])

    # Ensures model is abstract and not created in database
    class Meta:
        abstract = True

    ''' Overrides save method to ensure inventory is refreshed '''
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.inventory_item.items_purchased.add(self)
        self.inventory_item.refresh_from_db()

    ''' Overrides save method to ensure inventory is refreshed '''
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.inventory_item.items_purchased.remove(self)
        self.inventory_item.refresh_from_db()

''' Model for materials in a purchase '''
class PurchaseMaterial(PurchaseInventory):
    inventory_item = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='purchse_materials')

''' Model for tools in a purchase '''
class PurchaseTool(PurchaseInventory):
    inventory_item = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='purchase_tools')

''' Model for assets in a purchase '''
# class PurchaseAsset(AtomicOperationsMixin, models.Model):
#     purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='assets')
#     instance = models.ForeignKey(AssetInstance, on_delete=models.CASCADE)
#     usage = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
#     condition = models.CharField(max_length=21, choices=AssetInstance.CONDITION_CHOICES, default=AssetInstance.CONDITION_CHOICES.GOOD, validators=[MaxLengthValidator(17)])
#     cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0.0))])
