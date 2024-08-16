from django.views.generic import ListView, DetailView

from news.models import News, Category
from orders.views import ContextMixin


class NewsListView(ContextMixin, ListView):
    model = News
    template_name = "pages/news_list.html"
    paginate_by = 10
    ordering = "-published_date"

    def get_queryset(self):
        queryset = super().get_queryset()

        if category := self.request.GET.get("category"):
            queryset = queryset.filter(category__slug=category.lower())

        order_by = self.request.GET.get("sorting", "newest")
        if order_by == "oldest":
            queryset = queryset.order_by("published_date")
        else:
            queryset = queryset.order_by("-published_date")

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class NewsDetailView(ContextMixin, DetailView):
    model = News
    template_name = "pages/news_detail.html"
