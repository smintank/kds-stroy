from django.urls import path

from .views import SubscribeView


urlpatterns = [
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    # path("unsubscribe/", UnsubscribeView.as_view(), name="unsubscribe"),
]