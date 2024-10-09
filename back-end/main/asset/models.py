from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.utils import timezone
from django.db import models
from decimal import Decimal

# Asset model
class Asset(models.Model):
    class CONDITION_CHOICES(models.TextChoices):
        GOOD = 'good', 'Good'
        NEEDS_MAINTENANCE = 'needs maintenance', 'Needs Maintenance'
        OUT_OF_SERVICE = 'out of service', 'Out of Service'

    class STATUS_CHOICES(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        IN_USE = 'in use', 'In Use'
        UNDER_MAINTENANCE = 'under maintenance', 'Under Maintance'
        OUT_OF_SERVICE = 'out of service', 'Out of Service'

    def default_next_maintenance():
        return timezone.now() + timezone.timedelta(weeks=26)

    name = models.CharField(max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    serial_number = models.CharField(max_length=100, unique=True)
    description = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    rental_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    last_maintenance = models.DateField(default=timezone.now)
    next_maintenance = models.DateField(default=default_next_maintenance)
    usage = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    location = models.CharField(max_length=500, null=True, blank=True)
    condition = models.CharField(max_length=17, choices=CONDITION_CHOICES, default=CONDITION_CHOICES.GOOD, validators=[MaxLengthValidator(17)])
    status = models.CharField(max_length=17, choices=STATUS_CHOICES, default=STATUS_CHOICES.AVAILABLE, validators=[MaxLengthValidator(17)])
    notes = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])

# Asset Maintenance model
class AssetMaintenance(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_records')
    date = models.DateField(default=timezone.now)
    next_maintenance = models.DateField(default=Asset.default_next_maintenance)
    current_usage = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(Decimal(0.0))])
    condition = models.CharField(max_length=17, choices=Asset.CONDITION_CHOICES, default=Asset.CONDITION_CHOICES.GOOD, validators=[MaxLengthValidator(17)])
    status = models.CharField(max_length=17, choices=Asset.STATUS_CHOICES, default=Asset.STATUS_CHOICES.AVAILABLE, validators=[MaxLengthValidator(17)])
    notes = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])

    def save(self, *args, **kwargs):
        if self.date >= self.asset.last_maintenance:
            self.asset.usage = self.current_usage
            self.asset.last_maintenance = self.date
            if self.next_maintenance:
                self.asset.next_maintenance = self.next_maintenance
            else:
                self.asset.next_maintenance = self.date + timezone.timedelta(weeks=26)
            if self.condition:
                self.asset.condition = self.condition
            else:
                self.asset.condition = self.asset.CONDITION_CHOICES.GOOD
            if self.status:
                self.asset.status = self.status
            else:
                self.asset.status = self.asset.STATUS_CHOICES.AVAILABLE
            self.asset.save()
        super().save(*args, **kwargs)
