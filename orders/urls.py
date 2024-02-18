from django.urls import path

from orders.views import order

app_name = 'order'

urlpatterns = [
    path('', order, name='create'),
]
