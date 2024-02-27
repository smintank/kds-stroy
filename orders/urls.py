from django.urls import path

from orders.views import create_order

# app_name = 'order'

urlpatterns = [
    path('', create_order, name='home'),
]
