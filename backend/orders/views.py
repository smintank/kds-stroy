from django.db.models import Q
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView

from kds_stroy import settings
from .forms import OrderCreationForm
from .models import OrderPhoto, Order, Region, District, City, CityType
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
                },
                status=201,
            )
        else:
            return JsonResponse({"error": "Не получилось создать заявку"}, status=400)


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
        text_input = request.GET.get('term').strip().replace(", ", ",")
        text_input = text_input.split()[-1]
        queryset = City.objects.filter(name__icontains=text_input)

        suggestions = []
        for city in queryset:
            text_input = [f'{city.district.region}',
                          f'{city.type.short_name}\u00a0{city.name}']
            if city.is_district_shown:
                text_input.insert(1, f'{city.district.short_name}')
            suggestions.append(", ".join(text_input))

        return JsonResponse(suggestions, safe=False)
