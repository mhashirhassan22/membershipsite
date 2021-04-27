from allauth.account.forms import LoginForm, SignupForm
from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="-", to_field_name="id")
    city = forms.ModelChoiceField(queryset=City.objects.all().distinct(), empty_label="-")
    state = forms.ModelChoiceField(queryset=Region.objects.all().distinct(), empty_label="-")
    timezone = forms.ChoiceField(choices=[(x, x) for x in pytz.common_timezones])
    interest = forms.ChoiceField(choices=[(x.name, x.name) for x in Interest.objects.all().distinct()], required=False)
    error_message = UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
            'work_title',
            'credit_card',
            'business_name',
            'website',
            'address',
            'phone',
            'country',
            'city',
            'state',
            'timezone'
            
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


    
    def save(self, request):
        # Ensure you call the parent classes save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)
        for x in request.POST.getlist("checks[]"):
            print(x)
            obj = UserInterest()
            obj.user = user
            interest = Interest.objects.get(name=x)
            obj.interest = interest
            obj.save()

        return user