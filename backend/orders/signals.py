from asgiref.sync import sync_to_async
from django.db.models.signals import post_save
from django.dispatch import receiver
import telegram
from telegram.constants import ParseMode

from .models import Order, User
from kds_stroy.settings import TG_BOT_TOKEN
from .utils import format_phone_number, format_comment, format_datetime, \
    format_city


@receiver(post_save, sender=Order)
async def send_telegram_notification(sender, instance: Order, created,
                                     **kwargs):
    if created:
        address = await sync_to_async(format_city)(instance.city)
        address += f", {instance.address}" if instance.address else ""

        message = f'✅ *Новая заявка!*\n\n' \
                  f'№ {instance.order_id} от ' \
                  f'{format_datetime(instance.created_at, raw=True)}\n\n' \
                  f'👤 *Имя:* {instance.first_name}\n\n' \
                  f'📱 *Телефон:* {format_phone_number(instance.phone_number)}\n\n' \
                  f'📍 *Адрес:* {address}\n\n' \
                  f'💬 *Комментарий:*\n' \
                  f'{format_comment(instance.comment, 100)}\n'

        try:
            tg_ids = await sync_to_async(list)(
                User.objects.filter(is_notify=True).values_list("tg_id", flat=True)
            )
        except Exception as e:
            print(f"Fail to get users for TG notifications: {e}")
            return

        bot = telegram.Bot(token=TG_BOT_TOKEN)

        for tg_id in tg_ids:
            try:
                await bot.send_message(chat_id=tg_id, text=message,
                                       parse_mode=ParseMode.MARKDOWN)
            except telegram.error.BadRequest as e:
                print(f"Fail to send message to use {tg_id}: {e}\n"
                      f"Maybe user blocked bot or didn't start it yet.")
            except Exception as e:
                print(f"Unexpected error: {e}")
