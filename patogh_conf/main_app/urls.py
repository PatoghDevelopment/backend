from django.urls import path
from main_app.views import SignupApiView, SigninApiView,CityListCreateApi, PatoghDetail
from main_app.views import UserInfoApiView ,VerifyOTPView,ForgotPasswordView,ChangePasswordView
from django.urls.resolvers import URLPattern

from . import views
from .views import SignupApiView, SigninApiView, UserInfoApiView 

urlpatterns = [
    path('signup/', SignupApiView.as_view() , name = 'user_signup'),
    path('signin/', SigninApiView.as_view() , name = 'user_signin'),
    path('profile/',UserInfoApiView.as_view(), name = 'user_info'),
    path('verify/', VerifyOTPView.as_view(), name = 'verify'), #otp Verify
    path('password/forgot/', ForgotPasswordView.as_view(), name='forgot_password'), #forgot Password
    path('password/reset/', ChangePasswordView.as_view(), name='reset_password'), #Resetting the Password after Login
    path('cityList/', CityListCreateApi.as_view(), name='city_list'),
    # path('topuser/', TopUsersApiView.as_view(), name='top_user'),

    # Patogh paths
    path('patogh/detail/<uuid:pk>/', PatoghDetail.as_view(), name="patogh_detail"),


    path('profile/',UserInfoApiView.as_view(), name = 'user_info' ),
    # path('searchGatherings/', views.SearchDorehami),
    # path('addGathering/', views.AddDorehami),
    path('userprofile/', views.UserProfile)
]
