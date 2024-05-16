from django.urls import path

from orders.views import (LocationAutocompleteView, OrderCreateView,
                          OrderDetailView)

app_name = "orders"

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="create"),
    path("detail/<int:order_id>/", OrderDetailView.as_view(), name="detail"),
    path('autocomplete/location/',
         LocationAutocompleteView.as_view(),
         name='location_autocomplete'),
]
