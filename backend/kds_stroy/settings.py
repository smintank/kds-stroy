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
    "users.apps.UsersConfig",
    "news.apps.NewsConfig",
    "orders.apps.OrdersConfig",
    "main.apps.MainConfig",
    "ads_mailing.apps.AdsMailingConfig",
    "verify_email.apps.VerifyEmailConfig",
    "sass_processor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
LOGIN_URL = "login"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT"))
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

ZVONOK_API_KEY = os.getenv("ZVONOK_API_KEY")
ZVONOK_ENDPOINT = os.getenv("ZVONOK_ENDPOINT")
ZVONOK_CAMPAIGN_ID = os.getenv("ZVONOK_CAMPAIGN_ID")

PHONE_VERIFICATION_TIME_LIMIT = 300  # in seconds
PHONE_VERIFICATION_ATTEMPTS_LIMIT = 3  # with one phone number
PHONE_CHANGE_FREQUENCY_LIMIT = 30  # in days


USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_ADMIN_ID = os.getenv("TG_ADMIN_ID")
