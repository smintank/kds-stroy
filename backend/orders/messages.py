NEW_ORDER_TG_MSG = "✅ *Новая заявка!*\n" \
                   "№ {order_id} от {datetime}\n\n" \
                   "👤 *Имя:* {first_name}\n\n" \
                   "📱 *Телефон:* {phone}\n\n" \
                   "📍 *Адрес:* {address}\n\n" \
                   "💬 *Комментарий:*\n{comment}"

SUCCESS_ORDER_CREATION_MSG = "Заявка №{} успешно создана!"
SUCCESS_ORDER_CREATION_SUB_MSG = "{}, мы свяжемся с вами в ближайшее время!"
ERROR_ORDER_CREATION_MSG = "Не получилось создать заявку"

PHONE_MIN_LENGTH_ERROR_MSG = "Номер телефона должен содержать не меньше 11 цифр"
PHONE_MAX_LENGTH_ERROR_MSG = "Номер телефона должен содержать не больше 11 цифр"

PHOTO_FILE_TYPE_ERROR_MSG = "{} - не является поддерживаемым типом изображения"
PHOTO_MAX_SIZE_ERROR_MSG = "{} - превышает максимальный размер в {} Мб"
PHOTO_DUPLICATE_ERROR_MSG = "{} - является дубликатом другого загружаемого файла"
PHOTO_EMPTY_ERROR_MSG = "{} - пустой файл"
PHOTO_AMOUNT_ERROR_MSG = "Превышено максимальное количество загружаемых " \
                         "фотографий - {} шт. " \
                         "Фотографий не будет загружено - {} шт."

