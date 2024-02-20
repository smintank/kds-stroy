from django.http import HttpResponse
from django.shortcuts import render

from .forms import OrderCreationForm
from .models import OrderPhoto




def create_order(request):
    if request.method == "POST":
        order_form = OrderCreationForm(request.POST, request.FILES or None)
        photos = request.FILES.getlist('photo')
        if order_form.is_valid():
            order = order_form.save()
            if photos:
                for photo in photos:
                    OrderPhoto.objects.create(order=order, photo=photo)
            return HttpResponse('Form is valid', status=201)
        else:
            return HttpResponse('Form is not valid', status=400)
    else:
        order_form = OrderCreationForm()
        return render(
            request, 'pages/main.html', {"order_form": order_form}
        )


