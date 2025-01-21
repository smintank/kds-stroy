import logging

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.messages import OLD_MAIL_CHANGING_SUBJECT, OLD_MAIL_CHANGING_TEXT
from users.utils.base import token_generator

from users.tasks import send_email_message

logger = logging.getLogger(__name__)


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
    try:
        send_email_message.delay(subject, message, user.email)
    except Exception as e:
        logger.exception(f'Email verification failed: {e}')


def send_change_email(request, user, old_email):
    send_verification_email(request, user)
    try:
        send_email_message.delay(OLD_MAIL_CHANGING_SUBJECT,
                                 OLD_MAIL_CHANGING_TEXT.format(email=user.email),
                                 old_email)
    except Exception as e:
        logger.exception(f'Email verification failed: {e}')
