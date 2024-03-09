import requests
import logging

from kds_stroy.settings import (
    ZVONOK_API_KEY, ZVONOK_ENDPOINT, ZVONOK_CAMPAIGN_ID
)

logger = logging.getLogger(__name__)


def call_and_get_pin(phone_number, pincode=None):
    payload = {
        'public_key': ZVONOK_API_KEY,
        'campaign_id': ZVONOK_CAMPAIGN_ID,
        'phone': phone_number,
        'phone_suffix': pincode
    }
    try:
        response = requests.post(ZVONOK_ENDPOINT, data=payload)
        response.raise_for_status()
        print(response.json())
        pincode = response.json().get('data').get('pincode')
    except requests.exceptions.RequestException as e:
        logger.exception("Zvonok API request error: ", e)
    except requests.JSONDecodeError as e:
        logger.exception("Zvonok API response json error: ", e)
    except KeyError as e:
        logger.exception("Zvonok API response data error: ", e)
    except Exception as e:
        logger.exception("Zvonok API error: ", e)

    logger.info(pincode)
    return pincode
