from django import forms

from users.models import User


class UserRegistrationForm(forms.ModelForm):
    """Форма для создания нового пользователя."""

    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'placeholder': '********'}))
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(attrs={'placeholder': '********'}))

    class Meta:
        model = User
        fields = ('avatar', "username", "phone_number", "email", "last_name", "first_name", 'middle_name')
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Username'}),
            'phone_number': forms.TextInput(
                attrs={'placeholder': '+7-999-999-99-99'}),
            'email': forms.TextInput(
                attrs={'placeholder': 'username@mail.ru'}),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Иванов'}),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Иван'}),
            'middle_name': forms.TextInput(
                attrs={'placeholder': 'Иванович'}),
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
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone_number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].label = "Имя"
        self.fields["last_name"].label = "Фамилия"
        self.fields["email"].label = "Электронная почта"
        self.fields["phone_number"].label = "Номер телефона"

        self.fields["first_name"].widget.attrs.update({"class": "form-control"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["phone_number"].widget.attrs.update({"class": "form-control"})


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
