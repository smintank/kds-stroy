import logging

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView

from .forms import OrderCreationForm
from .messages import ERROR_ORDER_CREATION_MSG as ERROR_MSG
from .messages import SUCCESS_ORDER_CREATION_MSG as SUCCESS_MSG
from .messages import SUCCESS_ORDER_CREATION_SUB_MSG as SUCCESS_TXT
from .models import Order, OrderPhoto
from .tasks import send_telegram_message_async
from .utils import get_notified_users, get_order_message


logger = logging.getLogger(__name__)


class ContextMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_form"] = OrderCreationForm()

        order_id = self.request.session.get("order_id")
        order = Order.objects.filter(order_id=order_id).first()
        # order = Order.objects.get(order_id=order_id) if order_id else None
        if order and order.status in [Order.Status.COMPLETED, Order.Status.CANCELED]:
            self.request.session["order_id"] = None
            self.request.session["order_created"] = None

        if not self.request.user.is_authenticated:
            context["login_form"] = AuthenticationForm()
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)

        order_id = self.request.session.get("order_id")
        order_created = 1 if self.request.session.get("order_created") else 0

        response.set_cookie('order_id', order_id, max_age=360000)
        response.set_cookie('order_created', order_created, max_age=360000)
        return response


class OrderCreateView(View):
    def post(self, request):
        order_form = OrderCreationForm(request.POST, request.FILES)

        if order_form.is_valid():
            order = order_form.save()
            request.session["order_created"] = True
            request.session["order_id"] = order.order_id

            try:
                if not request.user.is_staff:
                    send_telegram_message_async.delay(
                        text=get_order_message(order, md_safe=True),
                        chat_ids=get_notified_users()
                    )
            except Exception as e:
                logger.error(e)

            return JsonResponse({"message": SUCCESS_MSG.format(order.order_id),
                                 "text": SUCCESS_TXT.format(order.first_name),
                                 "order_id": order.order_id}, status=201)
        else:
            logger.error(f"Order form errors: {order_form.errors}")
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
