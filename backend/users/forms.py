import re

from django import forms

from users.models import User, PhoneVerification


class UserRegistrationForm(forms.ModelForm):
    """Форма для создания нового пользователя."""

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "register__form-input",
                "type": "password",
                "autocomplete": "new-password",
                "placeholder": "Пароль*",
            }
        ),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "register__form-input",
                "type": "password",
                "autocomplete": "new-password",
                "placeholder": "Подтвердите пароль*",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "middle_name", "email", "phone_number")
        widgets = {
            "phone_number": forms.TextInput(
                attrs={
                    "class": "register__form-input",
                    "type": "tel",
                    "autocomplete": "tel",
                    "placeholder": "Телефон*",
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "register__form-input",
                    "type": "email",
                    "autocomplete": "email",
                    "placeholder": "E-mail*",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "register__form-input",
                    "text-name-input": "true",
                    "autocomplete": "family-name",
                    "placeholder": "Фамилия",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "register__form-input",
                    "text-name-input": "true",
                    "autocomplete": "given-name",
                    "placeholder": "Имя*",
                }
            ),
            "middle_name": forms.TextInput(
                attrs={
                    "class": "register__form-input",
                    "text-name-input": "true",
                    "autocomplete": "additional-name",
                    "placeholder": "Отчество",
                }
            ),
        }

    def save(self, commit=True):
        """Сохраняет нового пользователя."""
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
        return cleared_phone_number


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone_number",
        )
        widgets = {
            "phone_number": forms.TextInput(
                attrs={
                    "type": "tel",
                    "autocomplete": "tel",
                    "placeholder": "Номер телефона*",
                    "data-tel-input": "",
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "placeholder": "Электронная почта*",
                    "type": "email",
                    "autocomplete": "email",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Имя*",
                    "autocomplete": "given-name",
                    "text-name-input": "",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Фамилия",
                    "autocomplete": "family-name",
                    "text-name-input": "",
                }
            ),
            "middle_name": forms.TextInput(
                attrs={
                    "placeholder": "Отчество",
                    "text-name-input": "",
                    "autocomplete": "additional-name",
                }
            ),
            "address": forms.TextInput(
                attrs={"placeholder": "Адрес", "autocomplete": "street-address"}
            ),
        }


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
        widgets = {"pincode": forms.TextInput(attrs={"class": "ds_input"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound or not self.is_valid():
            self.initial["pincode"] = ""

    def clean_pincode(self):
        pincode = self.cleaned_data.get("pincode")
        if not re.match(r"^\d{4}$", pincode) or not pincode.isnumeric():
            raise forms.ValidationError("Пин-код должен состоять из 4-x цифр")
        return pincode
