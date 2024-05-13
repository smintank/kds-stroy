from urllib.parse import quote_plus

from django.core.cache import cache
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView
from django.conf import settings

from .forms import OrderCreationForm
from .messages import (
    SUCCESS_ORDER_CREATION_MSG as SUCCESS_MSG,
    SUCCESS_ORDER_CREATION_SUB_MSG as SUCCESS_TXT,
    ERROR_ORDER_CREATION_MSG as ERROR_MSG,
)
from .models import OrderPhoto, Order, City
from .utils import get_order_message, get_notified_users
from .tasks import send_telegram_message_async


class OrderCreateView(View):
    def post(self, request):
        order_form = OrderCreationForm(request.POST, request.FILES)

        if order_form.is_valid():
            order = order_form.save()
            request.session["order_created"] = True
            request.session["order_id"] = order.order_id

            send_telegram_message_async.delay(
                text=get_order_message(order, md_safe=True),
                chat_ids=get_notified_users()
            )

            return JsonResponse({"message": SUCCESS_MSG.format(order.order_id),
                                 "text": SUCCESS_TXT.format(order.first_name),
                                 "order_id": order.order_id}, status=201)
        else:
            return JsonResponse({"error": ERROR_MSG}, status=400)


class OrderDetailView(DetailView):
    model = Order
    slug_field = "order_id"
    slug_url_kwarg = "order_id"
    template_name = "pages/order_detail.html"
    context_object_name = "order"
    queryset = Order.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photos"] = OrderPhoto.objects.filter(order=self.object)
        context["MEDIA_URL"] = settings.MEDIA_URL
        return context


class LocationAutocompleteView(View):
    def get(self, request):
        text_input = request.GET.get('term', '').strip().replace(", ", ",")
        if not text_input:
            return JsonResponse([], safe=False)

        city_name = text_input.split()[-1]
        cache_key = f'autocomplete:{quote_plus(city_name)}'
        suggestions = cache.get(cache_key)

        if suggestions is None:
            cities = City.objects.filter(
                name__icontains=city_name
            )[:15]
            suggestions = [str(city) for city in cities]
            cache.set(cache_key, suggestions, timeout=60 * 5)

        return JsonResponse(suggestions, safe=False)
