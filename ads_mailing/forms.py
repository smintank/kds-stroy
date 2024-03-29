from django import forms

from ads_mailing.models import MailingList


class SubscribeForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)

    def clean_email(self):
        email = self.cleaned_data['email']
        if MailingList.objects.filter(email=email).exists():
            raise forms.ValidationError('Вы уже подписаны на рассылку!')
        return email
