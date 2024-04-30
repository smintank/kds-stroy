import hashlib

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
