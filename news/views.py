from django.views.generic import TemplateView


class NewsListView(TemplateView):
    template_name = 'pages/news_list.html'
