from supplier.models import Supplier, SupplierAddress
from django.contrib import admin

''' Register supplier model with django admin site '''
class SupplierAdmin(admin.ModelAdmin):
    pass

admin.site.register(Supplier, SupplierAdmin)

''' Register supplier address model with django admin site '''
class SupplierAddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(SupplierAddress, SupplierAddressAdmin)
