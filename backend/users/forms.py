import re

from django import forms
from django.contrib.auth import get_user_model

from users.models import PhoneVerification
from users.utils.phone_number import clean_phone_number

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "autocomplete": "new-password",
                "id": "id_registration_password"
            }
        ),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "autocomplete": "new-password",
                "id": "id_registration_password_2"
            }
        ),
    )

    class Meta:
        model = User
        fields = ("first_name", "middle_name", "last_name", "email", "phone_number",
                  # "city", "address"
                  )
        widgets = {
            # "city": forms.TextInput(),
            # "address": forms.TextInput(attrs={"id": "id_register_address"}),
            "phone_number": forms.TextInput(attrs={"type": "tel", "autocomplete": "tel"}),
            "email": forms.TextInput(attrs={"type": "email", "autocomplete": "email"}),
            "last_name": forms.TextInput(attrs={"autocomplete": "family-name"}),
            "first_name": forms.TextInput(attrs={"autocomplete": "given-name"}),
            "middle_name": forms.TextInput(attrs={"autocomplete": "additional-name"})
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают")
        return cd["password2"]

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        cleared_phone_number = re.sub(r"\D", "", phone_number)
        if len(cleared_phone_number) < 11:
            raise forms.ValidationError(
                "Номер телефона должен содержать не меньше 11 цифр"
            )
        if cleared_phone_number[:2] == "77":
            raise forms.ValidationError(
                "Номера Республики Казахстан (+77) - не поддерживаются"
            )
        return cleared_phone_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': field.label + "*" if field.required else field.label
            })


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "middle_name", "email", "phone_number", "city", "address", "is_notify",
        )
        widgets = {
            "city": forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add label text to placeholder in all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'placeholder': field.label})

        # If city credential was filled then we add city-id attribute to city field for profile form.
        if self.instance and self.instance.city_id:
            self.fields['city'].widget.attrs.update({'city-id': self.instance.city_id})

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number:
            return clean_phone_number(phone_number)
        return phone_number


class ChangeEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Новая электронная почта"
        self.fields["email"].widget.attrs.update({"class": "form-control"})


class ChangePhoneNumberForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("phone_number",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone_number"].label = "Новый номер телефона"
        self.fields["phone_number"].widget.attrs.update({"class": "form-control"})


class PhoneVerificationForm(forms.ModelForm):

    class Meta:
        model = PhoneVerification
        fields = ("pincode",)
        widgets = {"pincode": forms.TextInput(attrs={"class": "ds_input", "hidden": ""})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound or not self.is_valid():
            self.initial["pincode"] = ""

    def clean_pincode(self):
        pincode = self.cleaned_data.get("pincode")
        if not pincode:
            raise forms.ValidationError("Пин-код не может быть пустым")
        if not re.match(r"^\d{4}$", pincode) or not pincode.isnumeric():
            raise forms.ValidationError("Пин-код должен состоять из 4-x цифр")
        return pincode
