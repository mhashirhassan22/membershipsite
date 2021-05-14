from django.contrib import admin
from django.urls import path , include
from django.conf.urls import url
from .import views
from .views import *


app_name = 'users'
urlpatterns = [
        path('', index , name="index"),
        path('login/', login , name="login"),
        path('contactus/', contactus , name="contactus"),
        path('payment_details/', payment_details , name="payment_details"),
        path('signup/', signup , name="signup"),
        path('forgot-password/', forgot , name="forgot"),
        path('forgot-password-request/', requestcode , name="forget_password"),
        path('verify-password-request/', confirmcode , name="verify_code"),
        path('set-password/', set_password , name="set_password"),
        path('redirect-login/', login_again , name="login_again"),
        path('verify/payment/', verify_payment , name="verify-payment"),
        path('paypal-pay/', PaypalFormView.as_view(), name='paypal-pay'),
        path('paypal-sub/', PaypalSub, name='paypal-sub'),
        path('paypal-ips/', ips, name='paypal-ips'),
        path('process_subscription/', views.process_subscription, name='process_subscription'),
        path('paypal-return/', payment_success, name='paypal-return'),
        path('paypal-cancel/', PaypalCancelView.as_view(), name='paypal-cancel'),
]
