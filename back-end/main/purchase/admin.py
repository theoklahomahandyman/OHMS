from purchase.models import Purchase, PurchaseReciept, PurchaseMaterial, PurchaseTool
from django.contrib import admin

class PurchaseAdmin(admin.ModelAdmin):
    pass

class PurchaseRecieptAdmin(admin.ModelAdmin):
    pass

class PurchaseMaterialAdmin(admin.ModelAdmin):
    pass

class PurchaseToolAdmin(admin.ModelAdmin):
    pass

admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseReciept, PurchaseRecieptAdmin)
admin.site.register(PurchaseMaterial, PurchaseMaterialAdmin)
admin.site.register(PurchaseTool, PurchaseToolAdmin)
