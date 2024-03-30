from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.shortcuts import render

from ads_mailing.forms import SubscribeForm
from orders.forms import OrderCreationForm
from orders.models import Order


def handler404(request, exception):
    return render(request, "404.html", status=404)


class MainView(TemplateView):
    template_name = "pages/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_form"] = OrderCreationForm()
        context["subscribe_form"] = SubscribeForm()
        context["view_name"] = self.__class__.__name__

        order_id = self.request.session.get("order_id", None)
        if Order.objects.filter(order_id=order_id).exists():
            context["form_submitted"] = True
            context["order_id"] = order_id

        login_form = AuthenticationForm()
        context["login_form"] = login_form
        return context
