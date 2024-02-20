import re

from django import forms

from .models import Order


class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'phone_number', 'address', 'comment', 'photo')
        widgets = {
            'phone_number': forms.TextInput(
                attrs={'type': "tel", 'data-tel-input': "",
                       'placeholder': 'Номер телефона*'}),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Имя*', 'autocomplete': 'given-name'}),
            'address': forms.TextInput(
                attrs={'placeholder': 'Адрес',
                       'autocomplete': 'street-address'}),
            'comment': forms.TextInput(
                attrs={'placeholder': 'Опишите вашу задачу'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        cleared_phone_number = re.sub(r'\D', '', phone_number)
        if len(cleared_phone_number) < 11:
            raise forms.ValidationError(
                'Номер телефона должен содержать не меньше 11 цифр'
            )
        return cleared_phone_number
