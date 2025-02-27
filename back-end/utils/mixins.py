from django.db import transaction

''' Mixin to provide atomic save and delete operations with row locking '''
class AtomicOperationsMixin:

    ''' Override save method to ensure database transaction is atomic and handles race conditions '''
    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Lock the row if it exists
            self.__class__.objects.select_for_update().filter(pk=self.pk).first()
            super().save(*args, **kwargs)

    ''' Override delete method to ensure database transaction is atomic and handles race conditions '''
    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Lock the row if it exists
            self.__class__.objects.select_for_update().filter(pk=self.pk).first()
            super().delete(*args, **kwargs)
