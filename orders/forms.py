import re
from django import forms

from .models import Order


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    # def clean(self, data, initial=None):
    #     single_file_clean = super().clean
    #     if isinstance(data, (list, tuple)):
    #         result = [single_file_clean(d, initial) for d in data]
    #     else:
    #         result = single_file_clean(data, initial)
    #     return result


class OrderCreationForm(forms.ModelForm):
    photo = MultipleFileField(label='Фото', required=False)

    class Meta:
        model = Order
        fields = ['first_name', 'phone_number', 'address', 'comment', 'photo']
        widgets = {
            'phone_number': forms.TextInput(
                attrs={'type': "tel", 'data-tel-input': "",
                       'placeholder': 'Номер телефона*'}),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Имя*', 'autocomplete': 'given-name'}),
            'address': forms.TextInput(
                attrs={'placeholder': 'Адрес',
                       'autocomplete': 'street-address'}),
            'comment': forms.Textarea(
                attrs={
                    'placeholder': 'Опишите вашу задачу',
                    'class': 'id_comment',
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
