import logging

from celery import shared_task
from django.core.mail import send_mail

from kds_stroy.settings import DEFAULT_FROM_EMAIL

logger = logging.getLogger(__name__)


@shared_task
def send_email_message(subject: str, message: str, email: str) -> None:
    try:
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [email])
        logger.info(f"Email to {email} with subject {subject} sent successfully")
    except Exception as e:
        logger.error(f"Error sending email to {email}: {e}")
