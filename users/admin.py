from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class MyUserAdmin(UserAdmin):
    list_display = ("email", "phone_number", "first_name", "last_name", "is_staff")
    list_filter = ('email', 'is_superuser', 'is_active')
    list_display_links = ('email', 'phone_number')
    readonly_fields = ('last_login', 'date_joined', 'email')
    ordering = ["id"]


admin.site.register(User, MyUserAdmin)
