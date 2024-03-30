from django import forms

from ..ads_mailing.models import MailingList


class SubscribeForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.EmailInput(
            attrs={'class': 'stocks__form-input', 'autocomplete': 'email',
                   'type': 'email', 'placeholder': 'Введите ваш e-mail'}),
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if MailingList.objects.filter(email=email).exists():
            raise forms.ValidationError('Вы уже подписаны на рассылку!')
        return email
