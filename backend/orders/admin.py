from datetime import timedelta

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Order, OrderPhoto
from .utils import format_phone_number


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
    list_display = ("order_id", "first_name", "formatted_phone_number",
                    "comment", "address", "status", "formatted_created_at",
                    "display_photo_preview")
    list_filter = ("status", "created_at")
    list_display_links = ("order_id", "first_name", )
    list_editable = ('status',)
    search_fields = ("order_id", "first_name", "phone_number")
    readonly_fields = ("created_at",)
    ordering = ["created_at"]
    inlines = [OrderPhotoInline]
    fields = (
        "first_name",
        "phone_number",
        "comment",
        "city",
        "address",
        "status",
        "discount",
        "cost",
        "created_at",
    )

    def formatted_phone_number(self, obj):
        phone_number = obj.phone_number
        if phone_number:
            formatted_number = format_phone_number(phone_number)
            link = format_html('<a href="tel:{}">{}</a>', phone_number,
                               formatted_number)
            return link
        return ""

    def formatted_created_at(self, obj):
        if obj.created_at.date() == timezone.now().date():
            time = obj.created_at.strftime('%H:%M')
            return f'Сегодня, {time}'
        elif obj.created_at.date() == timezone.now().date() - timedelta(days=1):
            time = obj.created_at.strftime('%H:%M')
            return f'Вчера, {time}'
        return obj.created_at.strftime('%d.%m.%Y %H:%M')

    def display_photo_preview(self, obj):
        if order_photo := obj.orderphoto_set.all():
            html = ""
            for photo in order_photo.all():
                html += f'<a href="{photo.photo.url}" target="_blank">' \
                        f'    <img src="{photo.photo.url}" width="25" />' \
                        f'</a>'
            return format_html(html)
        return "Нет фото"


    # def photo_count(self, obj):
    #     count = obj.orderphoto_set.count()
    #     if count == 0:
    #         return "Нет фото"
    #     return f'{count} шт.'

    # photo_count.short_description = 'Количество фото'
    display_photo_preview.short_description = 'Фото'
    formatted_phone_number.short_description = 'Телефонный номер'
    formatted_created_at.short_description = 'Создан'


admin.site.register(Order, OrderAdmin)
