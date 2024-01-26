from django.urls import path

from orders.views import CreateOrderView

app_name = 'order'

urlpatterns = [
    path('', CreateOrderView.as_view(), name='create'),
]
