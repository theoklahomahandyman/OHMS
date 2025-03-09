from service.models import Service
from django.contrib import admin

''' Register service model with django admin site '''
class ServiceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Service, ServiceAdmin)
