import re

from django import forms

from .messages import PHONE_MAX_LENGTH_ERROR_MSG, PHONE_MIN_LENGTH_ERROR_MSG
from .models import Order, OrderPhoto
from .utils import handle_order_photos


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)


class OrderCreationForm(forms.ModelForm):
    photo = MultipleFileField(label="Фото", required=False)

    class Meta:
        model = Order
        fields = ["first_name", "phone_number", "city", "address", "comment", "photo"]
        widgets = {
            "phone_number": forms.TextInput(
                attrs={
                    "id": "order_phone_number",
                    "type": "tel",
                    "autocomplete": "tel",
                    "class": "order__form-input",
                    "placeholder": "Номер телефона*",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "id": "order_first_name",
                    "placeholder": "Имя*",
                    "autocomplete": "given-name",
                    "class": "order__form-input",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "id": "orderCity",
                    "autocomplete-url": "/locations/autocomplete/",
                    "class": "order__form-input",
                    "placeholder": "Город",
                    "autocomplete": "address-level2",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Адрес",
                    "class": "order__form-input",
                    "autocomplete": "street-address",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "placeholder": "Опишите вашу задачу",
                    "class": "order__form-textarea",
                }
            ),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        cleared_phone_number = re.sub(r"\D", "", phone_number)
        if len(cleared_phone_number) < 11:
            raise forms.ValidationError(
                PHONE_MIN_LENGTH_ERROR_MSG
            )
        if len(cleared_phone_number) > 11:
            raise forms.ValidationError(
                PHONE_MAX_LENGTH_ERROR_MSG
            )
        return cleared_phone_number

    def clean_photo(self):
        photos = handle_order_photos(self.files)
        return photos

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_photos(instance)
        return instance

    def save_photos(self, order):
        photos = self.cleaned_data.get("photo") or []
        for photo in photos:
            OrderPhoto.objects.create(order=order, photo=photo)
