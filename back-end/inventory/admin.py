from inventory.models import Material, Tool
from django.contrib import admin

''' Register material model with django admin site '''
class MaterialAdmin(admin.ModelAdmin):
    pass

admin.site.register(Material, MaterialAdmin)

''' Register tool model with django admin site '''
class ToolAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tool, ToolAdmin)
