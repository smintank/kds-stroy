from django.shortcuts import render
from django.views.generic import TemplateView

from ads_mailing.forms import SubscribeForm
from orders.views import ContextMixin


def handler404(request, exception):
    return render(request, "404.html", status=404)


class MainView(ContextMixin, TemplateView):
    template_name = "pages/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscribe_form"] = SubscribeForm()
        return context


class TermsView(ContextMixin, TemplateView):
    template_name = "pages/personal_terms.html"
