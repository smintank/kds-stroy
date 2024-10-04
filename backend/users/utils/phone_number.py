import re


def clean_phone_number(phone_number):
    cleaned_number = re.sub(r'\D', '', phone_number)
    if cleaned_number.startswith('8'):
        return '7' + cleaned_number[1:]
    return cleaned_number


def format_phone_number(phone_number):
    cleaned_number = clean_phone_number(phone_number)
    return f"+7 ({cleaned_number[1:4]}) {cleaned_number[4:7]}-{cleaned_number[7:9]}-{cleaned_number[9:]}"
