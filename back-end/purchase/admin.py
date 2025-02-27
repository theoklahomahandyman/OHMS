from purchase.models import Purchase, PurchaseReceipt, PurchaseMaterial, PurchaseTool
from django.contrib import admin

''' Register purchse model with django admin site '''
class PurchaseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Purchase, PurchaseAdmin)

''' Register purchse receipt model with django admin site '''
class PurchaseReceiptAdmin(admin.ModelAdmin):
    pass

admin.site.register(PurchaseReceipt, PurchaseReceiptAdmin)

''' Register purchse material model with django admin site '''
class PurchaseMaterialAdmin(admin.ModelAdmin):
    pass

admin.site.register(PurchaseMaterial, PurchaseMaterialAdmin)

''' Register purchse tool model with django admin site '''
class PurchaseToolAdmin(admin.ModelAdmin):
    pass

admin.site.register(PurchaseTool, PurchaseToolAdmin)
