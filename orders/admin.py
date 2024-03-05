from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "first_name", "phone_number", 'status', 'created_at')
    list_filter = ('status', 'created_at')
    list_display_links = ('order_id', "first_name")
    readonly_fields = ('order_id',)
    ordering = ['created_at']


admin.site.register(Order, OrderAdmin)
