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
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="-", to_field_name="id")
    city = forms.ModelChoiceField(queryset=City.objects.all().distinct(), empty_label="-")
    state = forms.ModelChoiceField(queryset=Region.objects.all().distinct(), empty_label="-")
    timezone = forms.ChoiceField(choices=[(x, x) for x in pytz.common_timezones])
    interest = forms.ChoiceField(choices=[(x.name, x.name) for x in Interest.objects.all().distinct()], required=False)
    servicearea = forms.ChoiceField(choices=[(x.name, x.name) for x in ServiceArea.objects.all().distinct()], required=False)
    # cc_number = CardNumberField(label='Card Number', required=False)
    # cc_expiry = forms.DateTimeField(required=False)
    # cc_code = SecurityCodeField(label='CVV/CVC', required=False)


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
        try:
            area = request.POST['servicearea']
            if(area):
                obj = UserInterest()
                obj.interest = ServiceArea.objects.get(id=area)
                obj.user = user
                obj.save()
        except:
            print("INTEREST NOT SAVED")

        for x in request.POST.getlist("checks[]"):
            obj = UserInterest()
            obj.user = user
            interest = Interest.objects.get(name=x)
            obj.interest = interest
            obj.save()

        # try:
        #     obj = CreditCard()
        #     obj.cc_number = request.POST['card_number']
        #     obj.cc_code = request.POST['card_code']
        #     obj.cc_expiry = request.POST['card_month'] + request.POST['card_year']
        #     print(obj.cc_expiry)
        #     obj.save()
        #     user.credit_card = obj
        #     user.save()
        # except:
        #     raise ValidationError(self.error_messages['Credit card number not correct'])

        return user
