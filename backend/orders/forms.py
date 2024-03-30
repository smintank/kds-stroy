import re
from django import forms

from .models import Order


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)


class OrderCreationForm(forms.ModelForm):
    photo = MultipleFileField(label='Фото', required=False)

    class Meta:
        model = Order
        fields = ['first_name', 'phone_number', 'address', 'comment', 'photo']
        widgets = {
            'phone_number': forms.TextInput(
                attrs={'type': "tel", 'autocomplete': 'tel',
                       'class': 'order__form-input',
                       'placeholder': 'Номер телефона*'}),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Имя*', 'autocomplete': 'given-name',
                    'class': 'order__form-input'
                }
            ),
            'address': forms.TextInput(
                attrs={'placeholder': 'Адрес',
                       'class': 'order__form-input',
                       'autocomplete': 'street-address'}),
            'comment': forms.Textarea(
                attrs={
                    'placeholder': 'Опишите вашу задачу',
                    'class': 'order__form-textarea'
                }
            ),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        cleared_phone_number = re.sub(r'\D', '', phone_number)
        if len(cleared_phone_number) < 11:
            raise forms.ValidationError(
                'Номер телефона должен содержать не меньше 11 цифр'
            )
        return cleared_phone_number
