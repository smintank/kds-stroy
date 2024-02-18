from django.shortcuts import render

from .forms import OrderCreationForm


def order(request):
    if request.method == "POST":
        order_form = OrderCreationForm(request.POST)
        if order_form.is_valid():
            order_form.save()
            return render(
                request,
                "registration/registration_done.html",
                {"order_form": order_form}
            )
    else:
        order_form = OrderCreationForm()
    return render(
        request,
        {"order_form": order_form}
    )


