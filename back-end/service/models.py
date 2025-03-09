from django.core.validators import MinLengthValidator, MaxLengthValidator
from utils.mixins import AtomicOperationsMixin
from django.db import models

''' Model for services '''
class Service(AtomicOperationsMixin, models.Model):
    name = models.CharField(unique=True, max_length=255, validators=[MinLengthValidator(2), MaxLengthValidator(255)])
    description = models.CharField(blank=True, null=True, max_length=500, validators=[MaxLengthValidator(500)])

    def __str__(self):
        return self.name
