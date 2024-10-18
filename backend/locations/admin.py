from django.contrib import admin
from .models import City


class CityAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(City, CityAdmin)
