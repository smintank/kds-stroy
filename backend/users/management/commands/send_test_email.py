from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from kds_stroy.settings import DEFAULT_FROM_EMAIL


# python manage.py send_test_email --to name@domain.com

class Command(BaseCommand):
    help = 'Отправить тестовое письмо'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            help='Email получателя',
            required=True,
        )

    def handle(self, *args, **options):
        recipient = options['to']
        try:
            send_mail(
                subject='Тестовое письмо',
                message='Это тестовое письмо, отправленное из Django.',
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
            )
            self.stdout.write(self.style.SUCCESS(f'Письмо успешно отправлено на {recipient}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка отправки письма: {e}'))
