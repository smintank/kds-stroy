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
    session['pincode'] = pincode
    session['last_call_timestamp'] = timezone.now().strftime(
        '%Y-%m-%d %H:%M:%S'
    )
    set_countdown_value(session, is_full=True)


def set_countdown_value(session, last_call_tz=None, is_full=False, is_empty=False):
    time_limit = PHONE_VERIFICATION_TIME_LIMIT or 360
    now_tz = timezone.now()

    if is_full:
        session['countdown'] = time_limit
        return
    if is_empty:
        session['countdown'] = 0
        return

    last_call_passed = now_tz - last_call_tz
    session['countdown'] = int(time_limit - last_call_passed.total_seconds())


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


def is_call_attempts_limit(request, phone_number=None) -> bool:
    if not request.user.is_authenticated:
        return False

    attempt_limit = PHONE_VERIFICATION_ATTEMPTS_LIMIT or 3

    call_attempts = PhoneVerification.objects.filter(
        user=request.user,
        phone_number=phone_number or request.user.phone_number
    )
    if not call_attempts:
        return False

    return call_attempts.count() >= attempt_limit


def is_time_limit(timestamp: timezone, limit: int) -> bool:
    if not timestamp:
        return False
    limit_timestamp = timestamp + timezone.timedelta(seconds=limit)
    return timezone.now() < limit_timestamp


def str_to_tz(timestamp):
    if not timestamp:
        return None
    return timezone.make_aware(
        timezone.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'),
        timezone=datetime.timezone.utc
    )
