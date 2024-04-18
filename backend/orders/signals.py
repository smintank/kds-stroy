from django.db.models.signals import post_save
from django.dispatch import receiver
import telegram

from .models import Order
from kds_stroy.settings import TG_ADMIN_ID, TG_BOT_TOKEN


def format_phone_number(phone: str) -> str:
    return f'+7 ({phone[:3]}) {phone[3:6]}-{phone[6:8]}-{phone[8:]}'


@receiver(post_save, sender=Order)
async def send_telegram_notification(sender, instance: Order, created, **kwargs):
    if created:
        created_at = instance.created_at.strftime('%d.%m.%Y %H:%M')
        phone_number = format_phone_number(instance.phone_number)

        message = f'Новая заявка №: {instance.order_id}\n' \
                  f'{created_at}\n\n' \
                  f'Имя: {instance.first_name}\n' \
                  f'Телефон: {phone_number}'

        bot = telegram.Bot(token=TG_BOT_TOKEN)

        await bot.send_message(chat_id=TG_ADMIN_ID, text=message)
