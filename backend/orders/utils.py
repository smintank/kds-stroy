import hashlib
import os
import uuid
from datetime import timedelta

from django.utils import timezone

from kds_stroy.settings import MAX_UPLOADED_PHOTO_SIZE
from orders.messages import NEW_ORDER_TG_MSG
from users.models import User


def handle_photos(photos) -> list:
    proper_photos = {}
    errors = []
    for photo in photos.lists():
        photo = photo[1][0]
        photo_name = f'Файл "{photo.name}"'
        if len(proper_photos) >= 5:
            break
        try:
            if photo.content_type not in ["image/jpeg", "image/png"]:
                raise ValueError(
                    photo_name + "не является поддерживаемым типом изображения"
                )
            if photo.size > 1024 * 1024 * MAX_UPLOADED_PHOTO_SIZE:
                raise ValueError(
                    photo_name + "превышает максимальный размер в "
                                 f"{MAX_UPLOADED_PHOTO_SIZE} Мб"
                )
            file_hash = hashlib.md5(photo.read()).hexdigest()
            if proper_photos and file_hash in proper_photos:
                raise ValueError(
                    photo_name + "является дубликатом другого загружаемого файла"
                )
        except ValueError as e:
            errors.append(str(e))
        else:
            proper_photos[file_hash] = photo
    if errors:
        [print(error) for error in errors]
    return list(proper_photos.values())


def format_phone_number(phone: str) -> str:
    return f'+7 ({phone[:3]}) {phone[3:6]}-{phone[6:8]}-{phone[8:]}'


def format_comment(comment: str, length: int = 50) -> str:
    if not comment:
        return '-'
    comment = comment.strip().replace('\n', ' ')
    return comment[:length] + '...' if len(comment) > length else comment


def make_safe_for_markdown(text):
    """
    Convert text to make it safe for Markdown in Telegram messages.
    """
    escape_chars = '_*[`'
    return ''.join(
        ['\\' + char if char in escape_chars else char for char in text]
    )


def get_full_city(city):
    region = f"{city.district.region}, "
    if city.is_district_shown:
        region += f"{city.district.short_name}, "
    return region + f"{city.type.short_name}\u00a0{city.name}"


def format_datetime(datetime, raw=False):
    datetime = timezone.localtime(datetime)
    if not raw:
        time = datetime.strftime('%H:%M')
        if datetime.date() == timezone.now().date():
            return f'Сегодня, {time}'
        elif datetime.date() == timezone.now().date() - timedelta(days=1):
            return f'Вчера, {time}'
    return datetime.strftime('%d.%m.%y %H:%M')


def get_unique_uid(model) -> str:
    while True:
        unique_order_number = str(uuid.uuid1().int)[:8]
        if not model.objects.filter(order_id=unique_order_number).exists():
            return unique_order_number


def get_upload_path(instance, filename):
    _, file_extension = os.path.splitext(filename)
    path = os.path.join("order_photos", str(instance.order.order_id))
    return os.path.join(path, f"photo{file_extension}")


def get_full_address(city, address):
    if city and address:
        return get_full_city(city) + ', ' + address
    elif city:
        return get_full_city(city)
    else:
        return address


def get_order_message(order, md_safe=False):
    data: dict[str: str] = {"first_name": order.first_name,
                            "phone_number": order.phone_number,
                            "address": order.address,
                            "comment": order.comment}

    data = {
        key: make_safe_for_markdown(value)
        for key, value in data.items() if md_safe
    }

    return NEW_ORDER_TG_MSG.format(
        order_id=order.order_id,
        datetime=format_datetime(order.created_at, raw=True),
        first_name=data["first_name"],
        phone=format_phone_number(data["phone_number"]),
        address=get_full_address(order.city, data["address"]),
        comment=format_comment(data["comment"], length=100)
    )


def get_notified_users() -> list[int]:
    users = User.objects.filter(is_notify=True).values_list("tg_id", flat=True)
    return list(users)
