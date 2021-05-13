from allauth.account.forms import LoginForm, SignupForm
from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from cities_light.models import City, Country, Region
from django.utils.translation import ugettext_lazy as _
import pytz

User = get_user_model()


class YourLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(YourLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update(
            {'type': 'email', 'class': 'form-control', 'placeholder': 'Email *'})
        self.fields['password'].widget.attrs.update(
            {'type': 'password', 'class': 'form-control', 'placeholder': 'Password *'})


class CustomSignupForm(UserCreationForm):
    phone = forms.CharField(max_length=14)


    error_message = UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'email',
            'password1',
            'phone',
            
        ]


    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'placeholder': field.title(), 'class': 'form-control'})
        


    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class CheckoutForm(forms.ModelForm):
    subscription_options = [
    ('1-month', '1-Month subscription ($10 USD/Mon)'),
    ('6-month', '6-Month subscription Save $10 ($50 USD/Mon)'),
    ('1-year', '1-Year subscription Save $30 ($90 USD/Mon)'),
    ]

class SubscriptionForm(forms.Form):
    subscription_options = [
    ('1-month', '1-Month subscription ($10 USD/Mon)'),
    ('6-month', '6-Month subscription Save $10 ($50 USD/Mon)'),
    ('1-year', '1-Year subscription Save $30 ($90 USD/Mon)'),
    ]
    plans = forms.ChoiceField(choices=subscription_options)
