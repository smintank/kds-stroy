from django.urls import path

from backend.orders.views import OrderCreateView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='create'),
    path('detail/<int:order_id>/', OrderDetailView.as_view(), name='detail'),
    # path('list/', list_order, name='list'),
]
