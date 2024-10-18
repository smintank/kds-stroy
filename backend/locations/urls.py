from django.urls import path

from locations.views import LocationAutocompleteView

app_name = "locations"

urlpatterns = [
    path('autocomplete/',
         LocationAutocompleteView.as_view(),
         name='autocomplete')
]
