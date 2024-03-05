from django.urls import path

from orders.views import CreateOrderView

app_name = 'order'

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create'),
    # path('detail/<int:pk>/', detail_order, name='detail'),
    # path('list/', list_order, name='list'),
]
