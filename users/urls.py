from django.contrib import admin
from django.urls import path
from .import views
from .views import *


app_name = 'users'
urlpatterns = [
        path('', index , name="index"),
        path('login/', login , name="login"),
        path('contactus/', contactus , name="contactus"),
        path('signup/', signup , name="signup"),
        path('forgot-password/', forgot , name="forgot"),
        path('forgot-password-request/', requestcode , name="forget_password"),
        path('verify-password-request/', confirmcode , name="verify_code"),
        path('set-password/', set_password , name="set_password"),
        path('redirect-login/', login_again , name="login_again"),
        path('verify/payment/', verify_payment , name="verify-payment"),
        path('payment/', payment , name="payment"),
]
