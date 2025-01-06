from purchase.models import Purchase, PurchaseReceipt, PurchaseMaterial, PurchaseTool
from django.contrib import admin

class PurchaseAdmin(admin.ModelAdmin):
    pass

class PurchaseReceiptAdmin(admin.ModelAdmin):
    pass

class PurchaseMaterialAdmin(admin.ModelAdmin):
    pass

class PurchaseToolAdmin(admin.ModelAdmin):
    pass

admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseReceipt, PurchaseReceiptAdmin)
admin.site.register(PurchaseMaterial, PurchaseMaterialAdmin)
admin.site.register(PurchaseTool, PurchaseToolAdmin)
