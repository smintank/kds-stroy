import datetime
import requests
import logging

from django.core.exceptions import ValidationError
from django.utils import timezone

from kds_stroy.settings import (
    ZVONOK_API_KEY, ZVONOK_ENDPOINT, ZVONOK_CAMPAIGN_ID,
    PHONE_VERIFICATION_TIME_LIMIT, PHONE_VERIFICATION_ATTEMPTS_LIMIT,
    PHONE_CHANGE_FREQUENCY_LIMIT
)
from users.models import PhoneVerification

logger = logging.getLogger(__name__)


def phone_validation_prepare(phone_number, session, user):
    phone_validation_request = PhoneVerification.objects.get_or_create(
        user=user, phone_number=phone_number
    )
    session['phone_number'] = phone_number
    session['object_id'] = phone_validation_request[0].id


def call_api_process(session, last_request, pincode=None):
    pincode = call_api_request(last_request.phone_number, pincode=pincode)
    last_request.pincode = pincode
    last_request.save()

    session['last_call_timestamp'] = timezone.now().strftime(
        '%Y-%m-%d %H:%M:%S'
    )


def get_countdown_value(timestamp: str) -> int:
    time_limit = PHONE_VERIFICATION_TIME_LIMIT or 360
    time_passed = get_left_time(timestamp)
    return min(time_limit, time_passed)


def get_left_time(timestamp: str) -> int:
    now = timezone.now()
    last_call_tz = timezone.make_aware(
        timezone.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'),
        timezone=datetime.timezone.utc
    )
    return int((now - last_call_tz).total_seconds())


def call_api_request(phone_number: str, pincode: str = None) -> str:
    """
    Request a call to the phone number with Zvonok API service.
    If pincode is not provided, a new pincode will be generated and returned.
    Phone number should be in international format, e.g. +79991234567
    """
    payload = {
        'public_key': ZVONOK_API_KEY,
        'campaign_id': ZVONOK_CAMPAIGN_ID,
        'phone': f'+{phone_number}',
        'phone_suffix': pincode
    }
    try:
        response = requests.post(ZVONOK_ENDPOINT, data=payload)
        response.raise_for_status()
        json_response = response.json()
        print(json_response)
        data = json_response.get('data')
        pincode = data.get('pincode')
    except requests.exceptions.RequestException as e:
        logger.exception("Zvonok API request error: ", e)
        raise ValidationError(
            "Ошибка при отправке запроса на звонок от Zvonok API"
        )
    except requests.JSONDecodeError as e:
        logger.exception("Zvonok API response json error: ", e)
        raise ValidationError(
            "Ошибка при преобразовании в json ответа от Zvonok API"
        )
    except KeyError as e:
        logger.exception("Zvonok API response data error: ", e)
        raise ValidationError(
            "Ошибка при получении значения по ключу из ответа от Zvonok API"
        )
    except Exception as e:
        logger.exception("Zvonok API error: ", e)
        raise ValidationError(
            "Неизвестная ошибка при запросе звонка от Zvonok API"
        )
    logger.info(pincode)

    return pincode


def is_phone_change_limit(request):
    frequency_limit = PHONE_CHANGE_FREQUENCY_LIMIT or 30
    start_date = timezone.now() - timezone.timedelta(days=frequency_limit)
    last_phone_change_tz = request.user.phone_number_change_date

    return start_date <= last_phone_change_tz


def is_numbers_amount_limit(request):
    frequency_limit = PHONE_CHANGE_FREQUENCY_LIMIT or 30
    attempts_limit = PHONE_VERIFICATION_ATTEMPTS_LIMIT or 3
    start_date = timezone.now() - timezone.timedelta(days=frequency_limit)

    last_month_unique_numbers = PhoneVerification.objects.filter(
        user=request.user,
        created_at__gte=start_date
    ).values_list('phone_number', flat=True).distinct()

    return len(last_month_unique_numbers) > attempts_limit


def is_limits_reached(request):
    if is_time_limit(request.session):
        return True
    if is_attempt_limit(request.user):
        return True


def is_attempt_limit(user, phone_number=None) -> bool:
    if not user.is_authenticated:
        return False

    phone_number = phone_number or user.phone_number
    attempt_limit = PHONE_VERIFICATION_ATTEMPTS_LIMIT or 3

    call_attempts = PhoneVerification.objects.filter(
        user=user,
        phone_number=phone_number or user.phone_number
    )
    if not call_attempts:
        return False

    return call_attempts.count() >= attempt_limit


def is_time_limit(session) -> bool:
    timestamp = session.get('last_call_timestamp')
    if not timestamp:
        return False
    time_limit = PHONE_VERIFICATION_TIME_LIMIT or 360

    return time_limit > get_left_time(timestamp)

