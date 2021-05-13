from django.shortcuts import render, redirect
from django.http import HttpResponse
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse , include
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
from .forms import SubscriptionForm, CheckoutForm
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import valid_ipn_received 
from django.dispatch import receiver

# @login_required
def index(request):
    if request.user.is_authenticated:
        return render(request, 'based.html', {})
    return render(request, 'homepage/home.html', {})

def payment(request):
    return render(request, 'payment_method.html', {})

def payment_details(request):
    return render(request, 'payment_details.html', {})

def contactus(request):
    if request.method == "GET":
        context = {}
        context['faq_list'] = FAQ.objects.all()
        return render(request, 'contactus.html', context)
    else:
        context = {}
        email = request.POST['email']
        message = request.POST['message']
        contact = Contact()
        try:
            contact.email = email
            contact.message = message
            contact.save()
            context['success'] = "Your message is received. We will Contact you soon!"
        except:
            context['fail'] = "OPS! We could not get your message. Please try again."
        return render(request, 'contact/contactus.html', context)

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
@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')

@csrf_exempt
def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')

@receiver(valid_ipn_received)
def paypal_ipn(sender, **kwargs):
    ipn_obj = sender
    return HttpResponse("Payment Recieved!")

def subscription(request):
    if request.method=="POST":
        f=SubscriptionForm(request.POST)
        if f.is_valid():
            request.session['subscription_plan'] = request.POST.get('plans')
            return redirect('/process_subscription')
    else:
        f=SubscriptionForm()
    return render(request,'subscription_form.html',locals())

def process_subscription(request):

    subscription_plan = request.session.get('subscription_plan')
    host = request.get_host()

    if subscription_plan == '1-month':
        price = "10"
        billing_cycle = 1
        billing_cycle_unit = "M"
    elif subscription_plan == '6-month':
        price = "50"
        billing_cycle = 6
        billing_cycle_unit = "M"
    else:
        price = "90"
        billing_cycle = 1
        billing_cycle_unit = "Y"
    
    #notify = request.build_absolute_uri(reverse('paypal-ipn'))
    cancel_url = '/payment_cancelled'
    print(cancel_url)
    done_url = '/payment_done'
    paypal_dict  = {
        "cmd": "_xclick-subscriptions",
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        "a3": price,  # monthly price
        "p3": billing_cycle,  # duration of each unit (depends on unit)
        "t3": billing_cycle_unit,  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "no_note": "1",  # remove extra notes (optional)
        'item_name': 'Content subscription',
        'custom': 1,     # custom data, pass something meaningful here
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),

        'return_url': 'http://{}{}'.format(host,
                                           done_url),
        'cancel_return': 'http://{}{}'.format(host,
                                             cancel_url),
    }

    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    return render(request, 'process_subscription.html', locals())

def membership(request):
    return render(request,'membership.html')
