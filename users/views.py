from django.shortcuts import render
from django.http import HttpResponse
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from cities_light.models import City, Country, Region
from .models import *
import os
from twilio.rest import Client
import pytz
from .models import User

@login_required
def index(request):
    context = {
        'cities': City.objects.all(),
        'regions': Region.objects.all(),
        'countries': Country.objects.all(),
        'timezone': pytz.common_timezones,
        'service': ServiceArea.objects.all()
    }
    return render(request, 'based.html', context)


def login(request):
    return render(request, 'logine.html')

def signup(request):
    return render(request, 'index.html')


def forgot(request):
    return render(request, 'forgot_password.html')


def requestcode(request):
    if request.method == 'GET':
        return render(request, 'forgot_password.html')
    else:
        email = request.POST['email']
        phone = request.POST['phone']
        try:
            exist = User.objects.get(email=email)
            if(exist and exist.phone and phone and exist.phone == phone):
                request.session['email'] = email
                request.session['phone'] = exist.phone
            else:
                return HttpResponse("Phone does not match the user")
        except:
            return HttpResponse("Unexpected Error...!")
    account_sid = 'AC25a06a6346e507691a44414a56dfd055'
    auth_token = '762bf7cce3514918e9c1dbe5c5c7931a'
    client = Client(account_sid, auth_token)
    if(request.session['phone']):
        verification = client.verify \
                            .services('VA7f2d07a28a78b9879da08b5875f66f50') \
                            .verifications \
                            .create(to=request.sesison['phone'], channel='sms')
    else:
        return HttpResponse("Error sending message, please try again later!")
    return render(request, 'change_password.html')


def confirmcode(request):
    if request.method == 'GET':
        return render(request, 'change_password.html')
    else:
        code = request.POST['code']
        account_sid = 'AC25a06a6346e507691a44414a56dfd055'
        auth_token = '762bf7cce3514918e9c1dbe5c5c7931a'
        client = Client(account_sid, auth_token)
        verification = client.verify \
                                .services('VA7f2d07a28a78b9879da08b5875f66f50') \
                                .verification_checks \
                                .create(to=request.sesison['phone'], code=code)
        print(verification.status)
        if(verification.status == 'pending'):
            return HttpResponse("NOT CORRECT PASSWORD")
        return render(request, 'confirm_password.html')



def set_password(request):
    if request.method == 'GET':
        return render(request, 'confirm_password.html')
    else:
        try:
            user = User.objects.filter(email=request.session['email'])
            print(request.session['email'])
            if(user):
                pass
            else:
                return HttpResponse("No user with this email")
            del request.session['email']
            del request.session['phone']
        except:
            return HttpResponse("User Not Found")
        p1 = request.POST['password1']
        p2 = request.POST['password2']
        user.set_password(p1)
        user.save()

        return HttpResponse("success in changing password. Please login again")
