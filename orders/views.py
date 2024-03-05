from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView

from .forms import OrderCreationForm
from .models import OrderPhoto, Order
from .utils import handle_photos


class CreateOrderView(View):

    def post(self, request):
        order_form = OrderCreationForm(request.POST, request.FILES or None)

        if order_form.is_valid():
            order = order_form.save()
            request.session['form_submitted'] = True
            request.session['order_id'] = order.order_id

            handled_photos = handle_photos(request.FILES)
            if handled_photos:
                for photo in handled_photos:
                    OrderPhoto.objects.create(order=order, photo=photo)

            return JsonResponse({
                'message': f'Заявка №{order.order_id} успешно создана!',
                'text': f'Мы свяжемся с вами в ближайшее время!'
            }, status=201)
        else:
            return JsonResponse({'error': 'Не получилось создать заявку'},
                                status=400)


class OrderDetailView(DetailView):
    model = Order
    slug_field = 'order_id'
    slug_url_kwarg = 'order_id'
    # template_name = 'orders/order_detail.html'
    # context_object_name = 'order'
    # queryset = Order.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = OrderPhoto.objects.filter(order=self.object)
        return context
