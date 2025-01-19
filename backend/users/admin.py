from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from verify_email.admin import LinkCounter

from orders.models import Order

from .models import User
from .utils.phone_number import format_phone_number


class OrderInlineForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'address': forms.Textarea(attrs={'rows': 1, 'cols': 40}),
        }


class OrderAdmin(admin.StackedInline):
    model = Order
    form = OrderInlineForm
    extra = 0
    readonly_fields = ("created_at",)
    fields = ("status",
              "comment",
              "city",
              "address",
              "created_at",)
    ordering = ["-created_at"]
    autocomplete_fields = ['city']


class MyUserAdmin(UserAdmin):
    list_display = (
        "email",
        "formatted_phone_number",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_superuser", "is_active")
    list_display_links = ("email", "formatted_phone_number")
    readonly_fields = ("last_login", "date_joined", "email")
    ordering = ["id"]
    inlines = [OrderAdmin]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональная информация",
         {"fields": ("first_name", "middle_name", "last_name", "phone_number")}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions"),
                           "classes": ("collapse",)}),
        ("Уведомления", {"fields": ("is_notify", "tg_id")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_staff:
            form.base_fields["is_notify"].disabled = True
        return form

    def formatted_phone_number(self, obj):
        phone_number = obj.phone_number
        if phone_number:
            formatted_number = format_phone_number(phone_number)
            link = format_html('<a href="tel:{}">{}</a>', phone_number, formatted_number)
            return link
        return "-"

    def has_add_permission(self, request):
        return False

    formatted_phone_number.short_description = 'Телефонный номер'


admin.site.register(User, MyUserAdmin)

admin.site.site_header = "КДС-Строй"
admin.site.site_title = "КДС-Строй"
admin.site.index_title = "Панель администратора"
admin.site.empty_value_display = "Не задано"
admin.site.unregister(Group)
admin.site.unregister(LinkCounter)
