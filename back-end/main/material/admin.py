from material.models import Material
from django.contrib import admin

class MaterialAdmin(admin.ModelAdmin):
    pass

admin.site.register(Material, MaterialAdmin)
