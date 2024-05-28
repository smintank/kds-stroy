from django.views.generic import ListView, DetailView

from news.models import News, Category
from orders.forms import OrderCreationForm
from orders.models import Order


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
        context["order_form"] = OrderCreationForm()
        context["view_name"] = self.__class__.__name__

        order_id = self.request.session.get("order_id")
        order = Order.objects.filter(order_id=order_id).first()
        if order and order.status in [Order.Status.COMPLETED,
                                      Order.Status.CANCELED]:
            self.request.session["order_id"] = None
            self.request.session["order_created"] = None

        # login_form = AuthenticationForm()
        # context["login_form"] = login_form
        return context


class NewsDetailView(DetailView):
    model = News
    slug_field = "pk"
    slug_url_kwarg = "pk"
    template_name = "pages/news_detail.html"
    context_object_name = "news"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_form"] = OrderCreationForm()
        context["view_name"] = self.__class__.__name__

        order_id = self.request.session.get("order_id")
        order = Order.objects.filter(order_id=order_id).first()
        if order and order.status in [Order.Status.COMPLETED,
                                      Order.Status.CANCELED]:
            self.request.session["order_id"] = None
            self.request.session["order_created"] = None

        # login_form = AuthenticationForm()
        # context["login_form"] = login_form
        return context
