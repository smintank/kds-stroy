import hashlib
import logging
import os
import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.datastructures import MultiValueDict

from kds_stroy.settings import MAX_UPLOAD_PHOTO_AMOUNT as MAX_PHOTO
from kds_stroy.settings import MAX_UPLOADED_PHOTO_SIZE
from orders.messages import (NEW_ORDER_TG_MSG, PHOTO_AMOUNT_ERROR_MSG,
                             PHOTO_DUPLICATE_ERROR_MSG, PHOTO_EMPTY_ERROR_MSG,
                             PHOTO_FILE_TYPE_ERROR_MSG,
                             PHOTO_MAX_SIZE_ERROR_MSG)
from users.utils.phone_number import format_phone_number

User = get_user_model()

logger = logging.getLogger(__name__)

MByte = 1024 * 1024


def handle_order_photos(photos: MultiValueDict) -> list:
    """Handle uploaded photos for order."""
    photos = list(photos.lists())
    photos_amount = len(photos)

    if photos_amount >= MAX_PHOTO:
        photos = photos[:MAX_PHOTO]
        skipped_photos_amount = photos_amount - MAX_PHOTO
        logger.info(PHOTO_AMOUNT_ERROR_MSG.format(
            MAX_PHOTO, skipped_photos_amount)
        )
    return get_proper_photo(photos)


def get_proper_photo(photos: list) -> list:
    """Check if uploaded photos are valid."""
    proper_photos = {}

    for photo in photos:
        photo = photo[1][0]
        photo_name = f'Файл "{photo.name}"'
        try:
            if photo.size == 0:
                raise ValueError(PHOTO_EMPTY_ERROR_MSG.format(photo_name))
            if photo.content_type not in ["image/jpeg", "image/png"]:
                raise ValueError(PHOTO_FILE_TYPE_ERROR_MSG.format(photo_name))
            if photo.size > MAX_UPLOADED_PHOTO_SIZE * MByte:
                raise ValueError(PHOTO_MAX_SIZE_ERROR_MSG.format(
                    photo_name, MAX_UPLOADED_PHOTO_SIZE
                ))
            file_hash = hashlib.md5(photo.read()).hexdigest()
            if file_hash in proper_photos:
                raise ValueError(PHOTO_DUPLICATE_ERROR_MSG.format(photo_name))
        except ValueError as e:
            logger.info(e)
        else:
            proper_photos[file_hash] = photo
    return list(proper_photos.values())


def format_comment(comment: str, length: int = 50) -> str:
    """Format comment to human-readable format."""
    if not comment:
        return '-'
    comment = comment.strip().replace('\n', ' ')
    return comment[:length] + '...' if len(comment) > length else comment


def make_safe_for_markdown(unsafe_text):
    """
    Convert text to make it safe for Markdown in Telegram messages.
    """
    escape_chars = '_*[`'
    return ''.join(
        ['\\' + char if char in escape_chars else char for char in unsafe_text]
    )


def get_full_city(city) -> str:
    """Make full city name with region and district."""
    region = f"{city.district.region}, "
    if city.is_district_shown:
        region += f"{city.district.short_name}, "
    return region + f"{city.type.short_name}\u00a0{city.name}"


def format_datetime(datetime, raw=False) -> str:
    """Format datetime to human-readable format.
    If raw is False, return 'today' or 'yesterday' instead of day number.
    """
    datetime = timezone.localtime(datetime)
    if not raw:
        time = datetime.strftime('%H:%M')
        if datetime.date() == timezone.now().date():
            return f'Сегодня, {time}'
        elif datetime.date() == timezone.now().date() - timedelta(days=1):
            return f'Вчера, {time}'
    return datetime.strftime('%d.%m.%y %H:%M')


def get_unique_uid(model) -> str:
    """Generate unique random order ID."""
    while True:
        unique_order_number = str(uuid.uuid1().int)[:8]
        if not model.objects.filter(order_id=unique_order_number).exists():
            return unique_order_number


def get_upload_path(instance, filename: str) -> str:
    """Create path for uploaded order photo."""
    _, file_extension = os.path.splitext(filename)
    path = os.path.join("order_photos", str(instance.order.order_id))
    return os.path.join(path, f"photo{file_extension}")


def get_full_address(city, address: str) -> str:
    """Combine city and address into one string."""
    if city and address:
        return get_full_city(city) + ', ' + address
    elif city:
        return get_full_city(city)
    else:
        return address


def get_order_message(order, md_safe: bool = False) -> str:
    """Create a message for Telegram bot with order details."""
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
    """Return list of Telegram IDs of admins who should be notified."""
    users = User.objects.filter(is_notify=True).values_list("tg_id", flat=True)
    return list(users)
