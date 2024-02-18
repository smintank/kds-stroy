from django.shortcuts import render

from .forms import OrderCreationForm


def order(request):
    if request.method == "POST":
        order_form = OrderCreationForm(request.POST)
        if order_form.is_valid():
            order_form.save()
            return render(
                request,
                'pages/main.html',
                {"order": order_form}
            )
    else:
        order_form = OrderCreationForm()
    return render(
        request,
        'pages/main.html',
        {"order_form": order_form}
    )


