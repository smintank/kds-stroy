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

        order_id = self.request.session.get("order_id")
        order = Order.objects.filter(order_id=order_id).first()
        if order and order.status in [Order.Status.COMPLETED, Order.Status.CANCELED]:
            self.request.session["order_id"] = None
            self.request.session["order_created"] = None

        # login_form = AuthenticationForm()
        # context["login_form"] = login_form
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super(MainView, self).render_to_response(context, **response_kwargs)

        order_id = self.request.session.get("order_id")
        order_created = 1 if self.request.session.get("order_created") else 0
        response.set_cookie('order_id', order_id, max_age=360000)
        response.set_cookie('order_created', order_created, max_age=360000)
        return response
