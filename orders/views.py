from django.views.generic import TemplateView


class CreateOrderView(TemplateView):
    template_name = 'pages/create_order.html'
