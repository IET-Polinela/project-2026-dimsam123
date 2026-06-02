from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'email', 'is_admin', 'is_member', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('is_admin', 'is_member')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('is_admin', 'is_member')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)