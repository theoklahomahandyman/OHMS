from django.contrib import admin
from user.models import User

''' Register admin user model with django admin site '''
class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
