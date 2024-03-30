from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Group


class MyUserAdmin(UserAdmin):
    list_display = ("email", "phone_number", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ('is_superuser', 'is_active')
    list_display_links = ('email', 'phone_number')
    readonly_fields = ('last_login', 'date_joined', 'email')
    ordering = ["id"]


admin.site.register(User, MyUserAdmin)

admin.site.site_header = "КДС-Строй"
admin.site.site_title = "КДС-Строй"
admin.site.index_title = "Панель администратора"
admin.site.empty_value_display = 'Не задано'
admin.site.unregister(Group)
