from django.urls import path

from backend.news.views import NewsListView

app_name = 'news'

urlpatterns = [
    path('', NewsListView.as_view(), name='list'),
]
