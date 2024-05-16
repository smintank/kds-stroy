import requests
import logging

from django.core.exceptions import ValidationError
from django.utils import timezone

from kds_stroy.settings import (
    ZVONOK_API_KEY,
    ZVONOK_ENDPOINT,
    ZVONOK_CAMPAIGN_ID,
    PHONE_VERIFICATION_TIME_LIMIT,
    PHONE_VERIFICATION_ATTEMPTS_LIMIT,
    PHONE_CHANGE_FREQUENCY_LIMIT,
)
from users.models import PhoneVerification

logger = logging.getLogger(__name__)


def phone_validation_prepare(phone_number, session, user):
    """
    Prepare phone validation request and store necessary data in session.
    """
    phone_validation_request, _ = PhoneVerification.objects.get_or_create(
        user=user, phone_number=phone_number
    )
    session["phone_number"] = phone_number
    session["request_id"] = phone_validation_request.id


def is_limited(obj, kwargs):
    if is_attempt_limit(obj.user):
        kwargs["is_attempt_limit"] = True
        return 0
    if is_time_limit(obj.last_call):
        return get_countdown_value(obj.last_call)
    return 0


def call_api_process(last_request, pincode=None):
    """
    Process API call to verify phone number.
    """
    pincode = call_api_request(last_request.phone_number, pincode)
    last_request.pincode = pincode
    last_request.last_call = timezone.now()
    last_request.save()
    return pincode


def get_countdown_value(timestamp) -> int:
    """
    Calculate remaining time for countdown based on timestamp.
    """
    limit_seconds = PHONE_VERIFICATION_TIME_LIMIT or 360
    passed_seconds = int((timezone.now() - timestamp).total_seconds())
    last_seconds = limit_seconds - passed_seconds
    return max(last_seconds, 0)


def call_api_request(phone_number: str, pincode: str = None) -> str:
    """
    Request a call to the phone number with Zvonok API service.
    """
    payload = {
        "public_key": ZVONOK_API_KEY,
        "campaign_id": ZVONOK_CAMPAIGN_ID,
        "phone": f"+{phone_number}",
        "phone_suffix": pincode,
    }
    response = None
    try:
        response = requests.post(ZVONOK_ENDPOINT, data=payload)
        response.raise_for_status()
        json_response = response.json()
        print(json_response)
        data = json_response.get("data")
        pincode = data.get("pincode")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            json = response.json()
            logger.exception("Bad Request to Zvonok API: " + json, exc_info=e)
        if response.status_code == 429:
            json = response.json()
            logger.exception("Limit exceeded to Zvonok API: " + json,
                             exc_info=e)
        else:
            logger.exception("HTTP Error: ", exc_info=e)
    except requests.RequestException as e:
        logger.exception("Zvonok API request error: ", exc_info=e)
        raise ValidationError("Error sending request to Zvonok API")
    except (requests.JSONDecodeError, KeyError) as e:
        logger.exception("Zvonok API response error: ", exc_info=e)
        raise ValidationError("Error parsing response from Zvonok API")
    except Exception as e:
        logger.exception("Zvonok API error: ", exc_info=e)
        raise ValidationError("Unknown error from Zvonok API")
    logger.info(pincode)
    return pincode


def is_phone_change_limit(number_change_date):
    """
    Check if the phone number change limit has been reached.
    """
    frequency_limit = PHONE_CHANGE_FREQUENCY_LIMIT or 30
    start_date = timezone.now() - timezone.timedelta(days=frequency_limit)
    return number_change_date > start_date


def is_numbers_amount_limit(request):
    """
    Check if the limit for the number of verification attempts has been reached
    """
    frequency_limit = PHONE_CHANGE_FREQUENCY_LIMIT or 30
    attempts_limit = PHONE_VERIFICATION_ATTEMPTS_LIMIT or 3
    start_date = timezone.now() - timezone.timedelta(days=frequency_limit)

    last_month_unique_numbers = (
        PhoneVerification.objects.filter(user=request.user,
                                         created_at__gte=start_date)
        .values_list("phone_number", flat=True)
        .distinct()
    )

    return len(last_month_unique_numbers) > attempts_limit


def is_attempt_limit(user) -> bool:
    """
    Check if the user has reached the verification attempts limit.
    """
    attempt_limit = PHONE_VERIFICATION_ATTEMPTS_LIMIT or 3
    call_attempts = PhoneVerification.objects.filter(
        user=user, phone_number=user.phone_number
    )
    return call_attempts.count() >= attempt_limit


def is_time_limit(timestamp) -> bool:
    """
    Check if the time limit for verification has been reached.
    """
    if not timestamp:
        return False
    limit_seconds = PHONE_VERIFICATION_TIME_LIMIT or 360
    passed_seconds = int((timezone.now() - timestamp).total_seconds())
    return passed_seconds <= limit_seconds
