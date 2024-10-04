from django.contrib.auth.forms import AuthenticationForm

from orders.forms import OrderCreationForm
from orders.models import Order
from users.utils.phone_number import format_phone_number


def global_context(request):
    context = {}
    user = request.user

    if not user.is_authenticated:
        context["order_form"] = OrderCreationForm()
        context["login_form"] = AuthenticationForm()
    else:
        city = user.city
        context["order_form"] = OrderCreationForm(initial={
            'first_name': user.first_name,
            'phone_number': format_phone_number(user.phone_number),
            'address': user.address,
            'city': str(city) if city else '',
            'city_id': city.id if city else ''
        })

    order_id = request.session.get("order_id")
    if order_id:
        order = Order.objects.filter(order_id=order_id).first()
        if order and order.status in [Order.Status.COMPLETED, Order.Status.CANCELED]:
            request.session.pop("order_id", None)
            request.session.pop("order_created", None)
    return context
