import hashlib

from django.http import JsonResponse
from django.shortcuts import render

from .forms import OrderCreationForm
from .models import OrderPhoto
from kds_stroy.settings import MAX_UPLOADED_PHOTO_SIZE


def handle_photos(photos):
    proper_photos = {}
    errors = []
    for photo in photos.lists():
        photo = photo[1][0]
        photo_name = f'Файл "{photo.name}"'
        if len(proper_photos) >= 5:
            break
        try:
            if photo.content_type not in ['image/jpeg', 'image/png']:
                raise ValueError(photo_name + 'не является поддерживаемым '
                                              'типом изображения')
            if photo.size > 1024 * 1024 * MAX_UPLOADED_PHOTO_SIZE:
                raise ValueError(photo_name + 'превышает максимальный размер в '
                                              f'{MAX_UPLOADED_PHOTO_SIZE} Мб')
            file_hash = hashlib.md5(photo.read()).hexdigest()
            if proper_photos and file_hash in proper_photos:
                raise ValueError(photo_name + 'является дубликатом другого '
                                              'загружаемого файла')
        except ValueError as e:
            errors.append(str(e))
        else:
            proper_photos[file_hash] = photo
    return list(proper_photos.values()), errors


def create_order(request):
    if request.method == "POST":
        order_form = OrderCreationForm(request.POST, request.FILES or None)

        if order_form.is_valid():
            order = order_form.save()

            handled_photos, errors = handle_photos(request.FILES)
            if handled_photos:
                for photo in handled_photos:
                    OrderPhoto.objects.create(order=order, photo=photo)
            if errors:
                [print(error) for error in errors]
            return JsonResponse({
                'message': f'Заявка №{order.order_id} успешно создана!',
                'text': f'Мы свяжемся с вами в ближайшее время!'
                }, status=201)
        else:
            return JsonResponse({'error': 'Не получилось создать заявку'},
                                status=400)
    else:
        order_form = OrderCreationForm()
        return render(request, 'pages/main.html', {"order_form": order_form})
