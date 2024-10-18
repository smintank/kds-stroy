import logging

from django.http import JsonResponse
from django.views import View

from .forms import OrderCreationForm
from .messages import ERROR_ORDER_CREATION_MSG as ERROR_MSG
from .messages import SUCCESS_ORDER_CREATION_MSG as SUCCESS_MSG
from .messages import SUCCESS_ORDER_CREATION_SUB_MSG as SUCCESS_TXT
from .tasks import send_telegram_message_async
from .utils import get_notified_users, get_order_message


logger = logging.getLogger(__name__)


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
