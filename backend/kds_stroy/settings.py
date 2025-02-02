import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "SECRET_KEY", default="p31bk+c$##k2@l%$pcxzjmm6*3g$s9(lp7dclwib6^c$0b0+h5"
)

DEBUG = bool(int(os.getenv("DEBUG", default=0)))

ALLOWED_HOSTS = str(os.getenv("ALLOWED_HOSTS")).split()

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "locations.apps.LocationsConfig",
    "users.apps.UsersConfig",
    "news.apps.NewsConfig",
    "orders.apps.OrdersConfig",
    "main.apps.MainConfig",
    "ads_mailing.apps.AdsMailingConfig",
    "verify_email.apps.VerifyEmailConfig",
    "sass_processor",
    "django_ckeditor_5",
    'widget_tweaks',
    'constance',
    'webp_converter',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'orders.middleware.OrderMiddleware',
]

AUTHENTICATION_BACKENDS = [
    "users.authentication.EmailPhoneUsernameBackend",
    "django.contrib.auth.backends.ModelBackend",
]

ROOT_URLCONF = "kds_stroy.urls"

TEMPLATES_DIR = BASE_DIR / "templates"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "orders.context_processor.global_context",
                'constance.context_processors.config',
                'webp_converter.context_processors.webp_support',
            ],
        },
    },
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "error.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

WSGI_APPLICATION = "kds_stroy.wsgi.application"

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INTERNAL_IPS = [
        '127.0.0.1',
    ]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    CSRF_TRUSTED_ORIGINS = [
        'https://kdsstroy.ru',
        'https://www.kdsstroy.ru'
    ]

    CSRF_COOKIE_DOMAIN = 'kdsstroy.ru'
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "django"),
            "USER": os.getenv("POSTGRES_USER", "django"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", ""),
            "PORT": os.getenv("DB_PORT", 5432),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.User"

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "static"

SASS_PROCESSOR_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGOUT_REDIRECT_URL = "home"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = bool(int(os.getenv("EMAIL_TLS", default=0)))
EMAIL_USE_SSL = bool(int(os.getenv("EMAIL_SSL", default=0)))
EMAIL_HOST_USER = os.environ.get("EMAIL_ID")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PW")
DEFAULT_FROM_EMAIL = os.environ.get("FROM_EMAIL")

VERIFICATION_SUCCESS_TEMPLATE = TEMPLATES_DIR / "registration/varification_done.html"
VERIFICATION_FAILED_TEMPLATE = TEMPLATES_DIR / "registration/varification_fail.html"
HTML_MESSAGE_TEMPLATE = TEMPLATES_DIR / "registration/verification_message.html"
REQUEST_NEW_EMAIL_TEMPLATE = "registration/new_email_request.html"
LINK_EXPIRED_TEMPLATE = "registration/expired.html"
NEW_EMAIL_SENT_TEMPLATE = "registration/new_email_sent.html"
EXPIRE_AFTER = "10m"
MAX_RETRIES = 3

MAX_UPLOADED_PHOTO_SIZE = 10  # in MB
MAX_UPLOAD_PHOTO_AMOUNT = 5

ZVONOK_API_KEY = os.getenv("ZVONOK_API_KEY")
ZVONOK_ENDPOINT = os.getenv("ZVONOK_ENDPOINT")
ZVONOK_CAMPAIGN_ID = os.getenv("ZVONOK_CAMPAIGN_ID")

PHONE_VERIFICATION_TIME_LIMIT = 300  # seconds between current and next call requests
PHONE_VERIFICATION_ATTEMPTS_LIMIT = 3  # call requests with one phone number
PHONE_CHANGE_FREQUENCY_LIMIT = 30  # days between two attempts of phone number changing
PINCODE_INPUT_LIMIT = 5  # trys to input pincode for every call request

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_ADMIN_ID = os.getenv("TG_ADMIN_ID")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

customColorPalette = [
    {
        'color': 'hsl(4, 90%, 58%)',
        'label': 'Red'
    },
    {
        'color': 'hsl(340, 82%, 52%)',
        'label': 'Pink'
    },
    {
        'color': 'hsl(291, 64%, 42%)',
        'label': 'Purple'
    },
    {
        'color': 'hsl(262, 52%, 47%)',
        'label': 'Deep Purple'
    },
    {
        'color': 'hsl(231, 48%, 48%)',
        'label': 'Indigo'
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue'
    },
]

CKEDITOR_5_CONFIGS = {
    'extends': {
        'toolbar': ['bold', 'italic', 'underline', 'strikethrough', '|',
                    'bulletedList', 'numberedList', 'todoList', '|',
                    'link', 'subscript', 'superscript'],
    },
}

CONSTANCE_CONFIG = {
    "PHONE_NUMBER_CONTACT": (os.getenv("PHONE_NUMBER_CONTACT"), 'Номер телефона в шапке страницы'),
    "WHATSAPP_CONTACT": (os.getenv("WHATSAPP_CONTACT"), 'Номер Whatsapp в шапке страницы'),
    "TELEGRAM_CONTACT": (os.getenv("TELEGRAM_CONTACT"), 'Telegram ID для связи'),
    "SUPPORT_EMAIL": (os.getenv("SUPPORT_EMAIL"), "Email службы поддержки сайта"),
    "WORKING_TIME": (os.getenv("WORKING_TIME"), "График работы"),
    "WORKING_REGION": (os.getenv("WORKING_REGION"), "Регион работы"),
    "BUSINESS_NAME": (os.getenv("BUSINESS_NAME"), "Юридическое имя организации"),
    "BUSINESS_ID": (os.getenv("BUSINESS_ID"), "ИНН организации"),
    "BUSINESS_REG_NUM": (os.getenv("BUSINESS_REG_NUM"), "ОГРНИП организации"),
    "SHOW_SALE_BANNER": (False, "Показывать ли баннер со скидкой"),
    "SALE_BANNER_AMOUNT": ("", "Размер скидки на баннере"),
    "SALE_BANNER_TEXT": ("", "Условия акции на баннере"),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'Контактные данные': ('PHONE_NUMBER_CONTACT', 'WHATSAPP_CONTACT', "TELEGRAM_CONTACT", "SUPPORT_EMAIL",
                          "WORKING_TIME", "WORKING_REGION"),
    "Юридические данные": ("BUSINESS_NAME", "BUSINESS_ID", "BUSINESS_REG_NUM"),
    'Скидочный баннер': ('SHOW_SALE_BANNER', "SALE_BANNER_AMOUNT", "SALE_BANNER_TEXT"),
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
