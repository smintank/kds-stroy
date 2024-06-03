from django import forms


class SubscribeForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class": "stocks__form-input",
                "autocomplete": "email",
                "type": "email",
                "placeholder": "Введите ваш e-mail",
            }
        ),
    )
