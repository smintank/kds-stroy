from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import News, Category, NewsPhoto


class RequiredInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(form.cleaned_data and not form.cleaned_data.get('DELETE', False) for form in self.forms):
            return
        raise ValidationError('Добавьте хотя бы одно изображение.')


class NewsPhotoInline(admin.TabularInline):
    model = NewsPhoto
    extra = 0
    fields = ('photo', 'photo_preview')
    readonly_fields = ('photo_preview',)
    formset = RequiredInlineFormSet


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = [NewsPhotoInline]
    fields = ('title', 'content', 'published_date', 'author', 'category')
    readonly_fields = ('created_at', 'updated_at')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slug', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
