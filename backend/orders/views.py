from urllib.parse import quote_plus

from django.core.cache import cache
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView

from kds_stroy import settings
from .forms import OrderCreationForm
from .models import OrderPhoto, Order, City
from .utils import handle_photos


class OrderCreateView(View):
    def post(self, request):
        order_form = OrderCreationForm(request.POST, request.FILES or None)

        if order_form.is_valid():
            order = order_form.save()
            request.session["order_created"] = True
            request.session["order_id"] = order.order_id

            handled_photos = handle_photos(request.FILES)
            if handled_photos:
                for photo in handled_photos:
                    OrderPhoto.objects.create(order=order, photo=photo)

            return JsonResponse(
                {
                    "message": f"Заявка №{order.order_id} успешно создана!",
                    "text": f"Мы свяжемся с вами в ближайшее время!",
                    "order_id": order.order_id,
                },
                status=201,
            )
        else:
            return JsonResponse({"error": "Не получилось создать заявку"},
                                status=400)


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
