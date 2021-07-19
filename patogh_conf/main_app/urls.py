from django.urls import path
from django.urls.resolvers import URLPattern
from main_app.views import SignupApiView, SigninApiView, UserInfoApiView ,VerifyOTPView,ForgotPasswordView,ChangePasswordView
urlpatterns = [
    path('signup/', SignupApiView.as_view() , name = 'user_signup'),
    path('signin/', SigninApiView.as_view() , name = 'user_signin'),
    path('profile/',UserInfoApiView.as_view(), name = 'user_info' ),
    path('verify/', VerifyOTPView.as_view(), name = 'verify'), #otp Verify
    path('password/forgot/', ForgotPasswordView.as_view(), name='forgot-password'), #forgot Password
    path('password/reset/', ChangePasswordView.as_view(), name='reset-password'), #Resetting the Password after Login

]