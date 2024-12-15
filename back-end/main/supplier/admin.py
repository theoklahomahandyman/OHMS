from supplier.models import Supplier, SupplierAddress
from django.contrib import admin

class SupplierAdmin(admin.ModelAdmin):
    pass

class SupplierAddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(SupplierAddress, SupplierAddressAdmin)
