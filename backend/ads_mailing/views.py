from django.http import JsonResponse
from django.views.generic import FormView

from ads_mailing.forms import SubscribeForm
from ads_mailing.messages import SUCCESS_SUBSCRIPTION_MSG
from ads_mailing.models import MailingList


class SubscribeView(FormView):
    form_class = SubscribeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscribe_form"] = context.pop("form")
        return context

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        MailingList.objects.get_or_create(email=email)
        return JsonResponse(
            {"message": SUCCESS_SUBSCRIPTION_MSG}, status=201
        )
