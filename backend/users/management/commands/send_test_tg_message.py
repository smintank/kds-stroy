import requests
from django.core.management.base import BaseCommand

from kds_stroy.settings import TG_BOT_TOKEN


# python manage.py send_test_tg_message 22334455

class Command(BaseCommand):
    help = 'Отправить тестовое сообщение'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            help='ID получателя',
            required=True,
        )

    def handle(self, *args, **options):
        recipient = options['to']
        base_url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}'
        text_api = f'{base_url}/sendMessage'

        try:
            requests.post(text_api, data={
                'chat_id': recipient,
                'text': "Тестовое сообщение со смайликом 🐥",
                'parse_mode': 'Markdown'
            })
            self.stdout.write(self.style.SUCCESS(f'Сообщение успешно отправлено на {recipient}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка отправки сообщения: {e}'))
