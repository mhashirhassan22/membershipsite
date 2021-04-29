from django.shortcuts import render, redirect
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
import json
from django.http import JsonResponse
from datetime import date

# @login_required
def index(request):
    if request.user.is_authenticated:
        return render(request, 'based.html', {})
    return render(request, 'landing_page.html', {})


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
                return render(request, 'forgot_password.html', {'error':'Phone does not match the user'})
        except:
            return render(request, 'forgot_password.html', {'error':'Credentials not correct.'})
    account_sid = 'AC25a06a6346e507691a44414a56dfd055'
    auth_token = '762bf7cce3514918e9c1dbe5c5c7931a'
    client = Client(account_sid, auth_token)
    try:
        verification = client.verify \
                            .services('VA7f2d07a28a78b9879da08b5875f66f50') \
                            .verifications \
                            .create(to=request.session['phone'], channel='sms')
    except:
        return render(request, 'forgot_password.html', {'error':'Incorrect phone number.'})
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
                                .create(to=request.session['phone'], code=code)
        print(verification.status)
        if(verification.status == 'pending'):
            return render(request, 'change_password.html', {'error':'Verification code does not match. Please try again.'})
        return render(request, 'confirm_password.html')



def set_password(request):
    if request.method == 'GET':
        return render(request, 'confirm_password.html')
    else:
        try:
            user = User.objects.get(email=request.session['email'])
            print(request.session['email'])
            if(user):
                pass
            else:
                return render(request, 'confirm_password.html', {'error':'User not found. Connect Interrupted!'})
            del request.session['email']
            del request.session['phone']
        except:
            return render(request, 'confirm_password.html', {'error':'User not found. Connect Interrupted!'})
        p1 = request.POST['password1']
        p2 = request.POST['password2']
        if(p1 and p2 and p1 == p2):
            user.set_password(p1)
            user.save()
        else:
            return render(request, 'confirm_password.html', {'error':'Password fields do not match'})

        return redirect("login_again")


def login_again(request):
    return render(request, 'login_again.html')



def verify_payment(request):
    if request.method == 'GET':
        return render(request, 'confirm_password.html')
    else:
        context = {}
        card_number = json.loads(request.POST.get("card_number"))
        card_code = json.loads(request.POST.get("card_code"))
        card_expiry = json.loads(request.POST.get("card_expiry"))
        print(card_expiry)
        print(card_number)
        print(card_code)
        obj = CreditCard()
        try:
            obj.cc_code = card_code
            obj.card_number = card_number
            if(card_expiry>date.today().month):
                print("AAAAAAAAAAAAA")
            obj.card_expiry = date.today()
            context['success'] = "VERified"

        except:
            context['fail'] = "fail"

        # obj.save()
        return JsonResponse(context)