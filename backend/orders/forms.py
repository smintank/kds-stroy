import re
from django import forms

from .models import Order, City, Region, District


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)


class LocationAutocompleteField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.model_mapping = {
            'region': Region,
            'district': District,
            'city': City,
        }
        super().__init__(*args, **kwargs)

    def get_suggestions(self, value):
        suggestions = []
        for model_name, model in self.model_mapping.items():
            queryset = model.objects.filter(name__icontains=value)
            if queryset.exists():
                suggestions.extend(queryset.values_list('name', flat=True))
        return suggestions

    def clean(self, value):
        if not value:
            return value
        value = value.split(", ")[-1].split()[-1]
        return City.objects.filter(name=value).first()

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['data-autocomplete-url'] = 'orders/autocomplete/location/'
        attrs["class"] = "order__form-input"
        attrs["placeholder"] = "Город"
        attrs["autocomplete"] = "address-level2"
        return attrs


class OrderCreationForm(forms.ModelForm):
    photo = MultipleFileField(label="Фото", required=False)
    city = LocationAutocompleteField()

    class Meta:
        model = Order
        fields = ["first_name", "phone_number", "city", "address", "comment", "photo"]
        widgets = {
            "phone_number": forms.TextInput(
                attrs={
                    "type": "tel",
                    "autocomplete": "tel",
                    "class": "order__form-input",
                    "placeholder": "Номер телефона*",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Имя*",
                    "autocomplete": "given-name",
                    "class": "order__form-input",
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
                "Номер телефона должен содержать не меньше 11 цифр"
            )
        return cleared_phone_number
