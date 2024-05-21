from django.views.generic import ListView, DetailView

from news.models import News, Category


class NewsListView(ListView):
    template_name = "pages/news_list.html"
    context_object_name = "news"
    queryset = News.published.all()
    paginate_by = 10
    ordering = "-published_date"
    model = News

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class NewsDetailView(DetailView):
    model = News
    slug_field = "pk"
    slug_url_kwarg = "pk"
    template_name = "pages/news_detail.html"
    context_object_name = "news"
