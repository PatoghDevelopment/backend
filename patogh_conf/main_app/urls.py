from django.urls import path
from .views import *


urlpatterns = [
    path('get_otp', SendOTP.as_view(), name='user_signup'),
    path('signup/', Signup.as_view(), name='signup'),
]
