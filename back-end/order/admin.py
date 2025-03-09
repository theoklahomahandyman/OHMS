from order.models import Order, OrderWorkLog, OrderCost, OrderPicture, OrderMaterial, OrderTool, OrderPayment, OrderWorker
from django.contrib import admin

''' Register order model with django admin site '''
class OrderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Order, OrderAdmin)

''' Register order work log model with django admin site '''
class OrderWorkLogAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrderWorkLog, OrderWorkLogAdmin)

''' Register order cost model with django admin site '''
class OrderCostAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrderCost, OrderCostAdmin)

''' Register order picture model with django admin site '''
class OrderPictureAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrderPicture, OrderPictureAdmin)

''' Register order material model with django admin site '''
class OrderMaterialAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrderMaterial, OrderMaterialAdmin)

''' Register order tool model with django admin site '''
class OrderToolAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrderTool, OrderToolAdmin)

''' Register order payment model with django admin site '''
class OrderPaymentAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrderPayment, OrderPaymentAdmin)

''' Register order worker model with django admin site '''
class OrderWorkerAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrderWorker, OrderWorkerAdmin)
