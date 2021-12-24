from django.urls import path
from rest_framework import views
from .views import *
from main_app.views import  PatoghDetail, PatoghDetailWithSearch
from main_app.views import UserInfoApiView , Signup
from django.urls.resolvers import URLPattern


urlpatterns = [
    #athentication paths
    path('get_otp', SendOTP.as_view(), name='user_signup'),
    path('signup/', Signup.as_view(), name='signup'),

    # Patogh paths
    path('patogh/detail/<uuid:pk>/', PatoghDetail.as_view(), name="patogh_detail"),
    path('patogh/list/', PatoghDetailWithSearch.as_view(), name="patogh_list_with_search"),

    #user paths
    path('profile/',UserInfoApiView.as_view(), name = 'user_info' ),
    path('userprofile/', UserProfileView.as_view())
]
