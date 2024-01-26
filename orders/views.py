from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class CreateOrderView(TemplateView):
    template_name = 'pages/create_order.html'