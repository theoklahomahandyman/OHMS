from order.models import Order, OrderWorkLog, OrderCost, OrderPicture, OrderMaterial, OrderTool, OrderPayment, OrderWorker
from django.contrib import admin

class OrderAdmin(admin.ModelAdmin):
    pass

class OrderWorkLogAdmin(admin.ModelAdmin):
    pass

class OrderCostAdmin(admin.ModelAdmin):
    pass

class OrderPictureAdmin(admin.ModelAdmin):
    pass

class OrderMaterialAdmin(admin.ModelAdmin):
    pass

class OrderToolAdmin(admin.ModelAdmin):
    pass

class OrderPaymentAdmin(admin.ModelAdmin):
    pass

class OrderWorkerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderWorkLog, OrderWorkLogAdmin)
admin.site.register(OrderCost, OrderCostAdmin)
admin.site.register(OrderPicture, OrderPictureAdmin)
admin.site.register(OrderMaterial, OrderMaterialAdmin)
admin.site.register(OrderTool, OrderToolAdmin)
admin.site.register(OrderPayment, OrderPaymentAdmin)
admin.site.register(OrderWorker, OrderWorkerAdmin)
