import logging

import requests
from celery import shared_task

from kds_stroy.settings import TG_BOT_TOKEN

logger = logging.getLogger(__name__)


@shared_task
def send_telegram_message(text: str, chat_ids: list[int]):
    base_url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}'
    text_api = f'{base_url}/sendMessage'

    failed_ids = set()

    for chat_id in chat_ids:
        try:
            requests.post(text_api, data={
                'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'
            })
        except requests.exceptions.RequestException as e:
            logger.error(f"Error while sending message to {chat_id}: {e}")
            failed_ids.add(chat_id)
        except Exception as e:
            logger.error(f"Unknown error while sending message to {chat_id}: {e}")
            failed_ids.add(chat_id)

    if failed_ids:
        logger.error(f"Error while sending message to {failed_ids}")
        return "ERRORS"
    logger.info(f"Telegram messages sent successfully!")
    return "OK"
