import logging

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from kds_stroy.settings import DEFAULT_FROM_EMAIL
from users.utils.base import token_generator

logger = logging.getLogger(__name__)


@shared_task
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


@shared_task
def send_email_message(subject, message, email):
    try:
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [email])
        logger.info(f"Email to {email} with subject {subject} sent successfully")
    except Exception as e:
        logger.error(f"Error sending email to {email}: {e}")
