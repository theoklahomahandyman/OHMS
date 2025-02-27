from customer.models import Customer
from django.contrib import admin

''' Register customer model with django admin site '''
class CustomerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)
