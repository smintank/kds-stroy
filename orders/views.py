from django.shortcuts import render

from .forms import OrderCreationForm


def order(request):
    if request.method == "POST":
        order_form = OrderCreationForm(request.POST, request.FILES)
        if order_form.is_valid():
            order_form.save()
            return JsonResponse({'message': 'Form submitted successfully'},
                                status=201)
    else:
        order_form = OrderCreationForm()
    return render(
        request,
        'pages/main.html',
        {"order_form": order_form}
    )


