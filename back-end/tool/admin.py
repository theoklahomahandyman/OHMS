from django.contrib import admin
from tool.models import Tool

class ToolAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tool, ToolAdmin)
