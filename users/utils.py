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


def call_api_process(request, phone_number=None, user=None, pincode=None):
    phone_number = phone_number or request.user.phone_number
    user = user or request.user

    pincode = call_api_request(phone_number, pincode)

    last_call_tz = PhoneVerification.objects.create(
        user=user,
        phone_number=phone_number,
        pincode=pincode
    ).created_at

    request.session['pincode'] = pincode
    set_countdown_value(request, last_call_tz)


def set_countdown_value(request, last_call_tz):
    time_limit = PHONE_VERIFICATION_TIME_LIMIT or 60
    now_tz = timezone.now()
    last_call_passed = now_tz - last_call_tz
    countdown_value = max(time_limit, last_call_passed.total_seconds())
    request.session['countdown'] = countdown_value


def call_api_request(phone_number: str, pincode: str = None) -> dict:
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
        raise ValidationError("Ошибка при отправке запроса на звонок")
    except requests.JSONDecodeError as e:
        logger.exception("Zvonok API response json error: ", e)
        raise ValidationError("Ошибка при обработке ответа от Zvonok API")
    except KeyError as e:
        logger.exception("Zvonok API response data error: ", e)
        raise ValidationError("Ошибка при обработке ответа от Zvonok API")
    except Exception as e:
        logger.exception("Zvonok API error: ", e)
        raise ValidationError("Ошибка при отправке запроса на звонок")
    logger.info(pincode)

    return pincode


def is_phone_change_limit(request):
    frequency_limit = PHONE_CHANGE_FREQUENCY_LIMIT or 30
    last_phone_change_tz = request.user.phone_number_change_date
    return (timezone.now() - last_phone_change_tz).days <= frequency_limit


def is_call_attempts_limit(request, phone_number=None) -> bool:
    attempt_limit = PHONE_VERIFICATION_ATTEMPTS_LIMIT or 3

    if not request.user.is_authenticated:
        return False
    call_attempts = PhoneVerification.objects.filter(
        user=request.user,
        phone_number=phone_number or request.user.phone_number
    )
    if not call_attempts:
        return False

    last_call_tz = call_attempts.order_by('-created_at').first().created_at
    request.session['last_call_timestamp'] = last_call_tz.strftime(
        '%Y-%m-%d %H:%M:%S'
    )
    return call_attempts.count() >= attempt_limit


def is_call_time_limit(request):
    time_limit = PHONE_VERIFICATION_TIME_LIMIT or 60
    last_call_tz = request.session.get('last_call_timestamp')
    if not last_call_tz:
        return False

    last_call_tz = timezone.make_aware(
        timezone.datetime.strptime(last_call_tz, '%Y-%m-%d %H:%M:%S')
    )
    now_tz = timezone.now()
    time_barrier_tz = now_tz - timezone.timedelta(seconds=time_limit)

    return last_call_tz > time_barrier_tz
