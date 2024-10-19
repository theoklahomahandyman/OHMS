from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.utils import timezone
from django.db import models
from decimal import Decimal

# Asset model
class Asset(models.Model):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    description = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])
    notes = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])

# Asset Instance model
class AssetInstance(models.Model):
    class CONDITION_CHOICES(models.TextChoices):
        GOOD = 'Good'
        MAINTENANCE_SCHEDULED = 'Maintenance Scheduled'
        MAINTENANCE_SOON = 'Maintenance Soon'
        NEEDS_MAINTENANCE = 'Needs Maintenance'
        OUT_OF_SERVICE = 'Out of Service'

    def default_last_maintenance():
        return timezone.now().date()

    def default_next_maintenance():
        return timezone.now().date() + timezone.timedelta(weeks=26)

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='instances')
    serial_number = models.CharField(max_length=100)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    rental_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    last_maintenance = models.DateField(default=default_last_maintenance)
    next_maintenance = models.DateField(default=default_next_maintenance)
    usage = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    location = models.CharField(max_length=500, null=True, blank=True)
    condition = models.CharField(max_length=21, choices=CONDITION_CHOICES, default=CONDITION_CHOICES.GOOD, validators=[MaxLengthValidator(17)])
    notes = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=['asset', 'serial_number'], name='unique_assetinstance_serial_number')]

# Asset Maintenance model
class AssetMaintenance(models.Model):
    instance = models.ForeignKey(AssetInstance, on_delete=models.CASCADE, related_name='maintenance_records')
    date = models.DateField(default=AssetInstance.default_last_maintenance)
    next_maintenance = models.DateField(default=AssetInstance.default_next_maintenance)
    current_usage = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    condition = models.CharField(max_length=21, choices=AssetInstance.CONDITION_CHOICES, default=AssetInstance.CONDITION_CHOICES.GOOD, validators=[MaxLengthValidator(17)])
    notes = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])

    def save(self, *args, **kwargs):
        if self.date >= self.instance.last_maintenance:
            self.instance.last_maintenance = self.date
            if not self.next_maintenance:
                self.next_maintenance = self.date + timezone.timedelta(weeks=26)
            self.instance.next_maintenance = self.next_maintenance
            if self.current_usage == 0:
                self.current_usage = self.instance.usage
            self.instance.usage = self.current_usage
            if not self.condition:
                self.condition = self.instance.CONDITION_CHOICES.GOOD
            self.instance.condition = self.condition
            self.instance.save()
        super().save(*args, **kwargs)
