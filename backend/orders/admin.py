from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Order, OrderPhoto
from .utils import format_comment, format_datetime
from users.utils.phone_number import format_phone_number


class OrderPhotoInline(admin.TabularInline):
    model = OrderPhoto
    extra = 0
    readonly_fields = ('photo_preview',)
    fields = ('photo_preview',)

    def photo_preview(self, obj):
        html_block = f'<a href="{obj.photo.url}" target="_blank">' \
                     f'<img src="{obj.photo.url}" width="200">' \
                     '</a>'
        return mark_safe(html_block)


class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['city']
    list_display = ("order_id", "first_name", "formatted_phone_number",
                    "formatted_comment", "city", "status",
                    "formatted_created_at", "display_photo_preview")
    list_filter = ("status", "created_at")
    list_display_links = ("order_id", "first_name", )
    list_editable = ('status',)
    search_fields = ("order_id", "first_name", "phone_number")
    readonly_fields = ("created_at", "formatted_discount", "final_cost")
    ordering = ["-created_at"]
    inlines = [OrderPhotoInline]
    fieldsets = (
        (None, {
            "fields": (
                "first_name",
                "phone_number",
                "comment",
                "city",
                "address",
                "status",
                "created_at",
            )
        }),
        ("Стоимость", {
            "fields": (
                ("discount", "formatted_discount"),
                "cost",
                "final_cost",
            )
        }),
    )

    def formatted_phone_number(self, obj):
        phone_number = obj.phone_number
        if phone_number:
            formatted_number = format_phone_number(phone_number)
            link = format_html('<a href="tel:{}">{}</a>', phone_number, formatted_number)
            return link
        return "-"

    def formatted_discount(self, obj):
        return str(float(obj.cost) / 100 * float(obj.discount))

    def formatted_comment(self, obj):
        return format_comment(obj.comment)

    def formatted_created_at(self, obj):
        return (format_datetime(obj.created_at, raw=True)
                if obj.created_at else "-")

    def display_photo_preview(self, obj):
        if order_photo := obj.orderphoto_set.all():
            html = ""
            for photo in order_photo.all():
                html += f'<a href="{photo.photo.url}" target="_blank">' \
                        f'<img src="{photo.photo.url}" width="25" />' \
                        f'</a>'
            return format_html(html)
        return "-"

    formatted_discount.short_description = 'Скидка в рублях'
    formatted_comment.short_description = 'Комментарий'
    display_photo_preview.short_description = 'Фото'
    formatted_phone_number.short_description = 'Телефонный номер'
    formatted_created_at.short_description = 'Создан'


admin.site.register(Order, OrderAdmin)
