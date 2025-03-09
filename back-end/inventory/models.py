from django.core.validators import MinLengthValidator, MaxLengthValidator
from utils.mixins import AtomicOperationsMixin
from django.db import models
from decimal import Decimal

''' Base model for inventory items with shared properties '''
class InventoryItemBase(models.Model):
    # Ensures model is abstract and not created in database
    class Meta:
        abstract = True

    ''' Dynamically calculate available quantity based on purchases and orders '''
    @property
    def available_quantity(self):
        total_purchased = self.items_purchased.all().aggregate(total=models.Sum('quantity'))['total'] or 0
        if hasattr(self, 'items_used'):
            total_used = self.items_used.all().aggregate(total=models.Sum('quantity'))['total'] or 0
        elif hasattr(self, 'items_broken'):
            total_used = self.items_broken.all().aggregate(total=models.Sum('quantity_broken'))['total'] or 0
        else:
            total_used = 0
        return max(total_purchased - total_used, 0)

    ''' Dynamically calculate unit cost based on latest purchase '''
    @property
    def unit_cost(self):
        latest_purchase = self.items_purchased.all().order_by('-id').first()
        if latest_purchase and latest_purchase.quantity > 0:
            return Decimal(float(latest_purchase.cost / latest_purchase.quantity)).quantize(Decimal('0.01'))
        return Decimal(0.0).quantize(Decimal('0.01'))

''' Model for materials '''
class Material(AtomicOperationsMixin, InventoryItemBase):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    description = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])
    size = models.CharField(max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    items_purchased = models.ManyToManyField('purchase.PurchaseMaterial', related_name='materials')
    items_used = models.ManyToManyField('order.OrderMaterial', related_name='materials')

    class Meta:
        constraints = [ models.UniqueConstraint(fields=['name', 'size'], name='unique_material') ]

''' Model for tools '''
class Tool(AtomicOperationsMixin, InventoryItemBase):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    description = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])
    items_purchased = models.ManyToManyField('purchase.PurchaseTool', related_name='tools')
    items_broken = models.ManyToManyField('order.OrderTool', related_name='tools')
