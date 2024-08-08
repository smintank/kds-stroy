from urllib.parse import quote_plus

from django.core.cache import cache
from django.http import JsonResponse
from django.views import View

from .models import City


class LocationAutocompleteView(View):
    def get(self, request):
        text_input = request.GET.get('term', '').strip().replace(", ", ",")
        if not text_input:
            return JsonResponse([], safe=False)

        city_name = text_input.split()[-1]
        cache_key = f'autocomplete:{quote_plus(city_name)}'
        suggestions = cache.get(cache_key)

        if suggestions is None:
            cities = City.objects.filter(name__icontains=city_name)[:15]
            suggestions = [[city.id, str(city)] for city in cities]
            cache.set(cache_key, suggestions, timeout=60 * 5)

        return JsonResponse(suggestions, safe=False)
