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


    
    def save(self, request):
        # Ensure you call the parent classes save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

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


class SubscriptionForm(forms.Form):
    plans = forms.ModelChoiceField(queryset=MembershipPlan.objects.all())
