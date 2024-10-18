import logging

import requests
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

from kds_stroy.settings import (PHONE_CHANGE_FREQUENCY_LIMIT, PHONE_VERIFICATION_ATTEMPTS_LIMIT,
                                PHONE_VERIFICATION_TIME_LIMIT, ZVONOK_API_KEY, ZVONOK_CAMPAIGN_ID,
                                ZVONOK_ENDPOINT, DEFAULT_FROM_EMAIL)
from users.models import PhoneVerification
from users.utils.phone_number import clean_phone_number

logger = logging.getLogger(__name__)


token_generator = default_token_generator


def phone_validation_prepare(phone_number, session, user):
    """
    Prepare phone validation request and store necessary data in session.
    """
    phone_validation_request, _ = PhoneVerification.objects.get_or_create(
        user=user, phone_number=phone_number
    )
    session["phone_number"] = phone_number
    session["request_id"] = phone_validation_request.id


def get_countdown(obj, kwargs):
    if is_call_attempt_limit(obj.user):
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


def call_api_request(phone_number: str, pincode: str = None, timeout: int = 10) -> str:
    """
    Request a call to the phone number with the Zvonok API service.
    """
    payload = {
        "public_key": ZVONOK_API_KEY,
        "campaign_id": ZVONOK_CAMPAIGN_ID,
        "phone": f"+{clean_phone_number(phone_number)}",
        "phone_suffix": pincode,
    }

    response = None
    logger.debug(f"Payload prepared: {payload}")

    try:
        logger.debug("Sending request to Zvonok API...")
        response = requests.post(ZVONOK_ENDPOINT, data=payload, timeout=timeout, verify=False)
        response.raise_for_status()

        logger.debug("Received response from Zvonok API")
        json_response = response.json()
        logger.debug(f"Response JSON: {json_response}")

        data = json_response.get("data")
        pincode = data.get("pincode")
        logger.debug(f"Pincode received: {pincode}")

    except requests.exceptions.Timeout as e:
        logger.error(f"Request to Zvonok API timed out: {str(e)}", exc_info=e)
        raise ValidationError("Request to Zvonok API timed out")

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error: {response.status_code} - {response.text}", exc_info=e)
        if response.status_code == 400:
            json_data = response.json()
            logger.error(f"Bad request error from Zvonok API: {json_data.get('data')}", exc_info=e)
        elif response.status_code == 429:
            json_data = response.json()
            logger.error(f"Rate limit exceeded for Zvonok API: {json_data.get('data')}", exc_info=e)
        raise ValidationError("HTTP error occurred while contacting Zvonok API")

    except requests.RequestException as e:
        logger.error(f"Error during API request to Zvonok: {str(e)}", exc_info=e)
        raise ValidationError("Error sending request to Zvonok API")

    except (requests.JSONDecodeError, KeyError) as e:
        logger.error(f"Error parsing response from Zvonok API: {str(e)}", exc_info=e)
        raise ValidationError("Invalid response format from Zvonok API")

    except Exception as e:
        logger.error(f"Unexpected error in Zvonok API: {str(e)}", exc_info=e)
        raise ValidationError("An unknown error occurred with Zvonok API")

    if pincode:
        logger.info(f"Pincode successfully retrieved: {pincode}")
    else:
        logger.warning("Pincode not retrieved from Zvonok API")

    return pincode


def is_phone_change_limit(number_change_date) -> bool:
    """
    Check if the phone number change limit has been reached.
    """
    frequency_limit = PHONE_CHANGE_FREQUENCY_LIMIT or 30
    start_date = timezone.now() - timezone.timedelta(days=frequency_limit)
    return number_change_date > start_date


def is_numbers_amount_limit(user) -> bool:
    """
    Check if the limit for the number of verification attempts has been reached
    """
    frequency_limit = PHONE_CHANGE_FREQUENCY_LIMIT or 30
    attempts_limit = PHONE_VERIFICATION_ATTEMPTS_LIMIT or 3
    start_date = timezone.now() - timezone.timedelta(days=frequency_limit)

    last_month_unique_numbers = (
        PhoneVerification.objects.filter(user=user, created_at__gte=start_date)
                                 .values_list("phone_number", flat=True)
                                 .distinct()
    )

    return len(last_month_unique_numbers) > attempts_limit


def is_call_attempt_limit(user) -> bool:
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


def send_verification_email(request, user):
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verification_url = request.build_absolute_uri(
        reverse('users:email_verification', kwargs={'uidb64': uid, 'token': token})
    )

    subject = 'Верификация электронной почты'
    message = render_to_string('account/email_verification.html', {
        'user': user,
        'verification_url': verification_url,
    })
    send_email_message(subject, message, user.email)


def send_email_message(subject, message, email):
    try:
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [email])
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")
