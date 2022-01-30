from django.urls import path
from rest_framework import views
from .views import *
from .views import  PatoghDetailLimitedColumn
from .views import UserInfoApiView , Signup
from django.urls.resolvers import URLPattern


urlpatterns = [
    #athentication paths
    path('get_otp/', SingUpSendOTP.as_view(), name='user_signup'),
    path('signup/', Signup.as_view(), name='signup'),
    path('signin/', Signin.as_view(), name='signin'),
    path('reset_password_otp/', ResetPasswordSendOTP.as_view(), name='reset_password_otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),


    # Patogh paths
    path('patogh/detail/<uuid:pk>/', PatoghDetail.as_view(), name="patogh_detail"),
    path('patogh/detail/limit/<uuid:pk>/', PatoghDetailLimitedColumn.as_view(), name="patogh_detail_limited_column"),
    # path('patogh/list/', PatoghDetailWithSearch.as_view(), name="patogh_list_with_search"),

    #user paths
    path('profile/',UserInfoApiView.as_view(), name = 'user_info' ),
    # path('userprofile/', UserProfileView.as_view()),

    # users parties
    path('parties/', UserParties.as_view(), name="user_parties"),
]