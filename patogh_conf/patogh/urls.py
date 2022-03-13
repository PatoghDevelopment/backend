"""patogh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import gettext as _
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from main_app import views as app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('patogh/', include('main_app.urls')),
    path('signupotp/', app.SignupOTP.as_view(), name='Signup OTP'),
    path('signup/', app.Signup.as_view(), name='Signup'),
    path('signin/', app.Signin.as_view(), name='Signin'),
    path('forgotpasswordotp/', app.ForgotPasswordSendOTP.as_view(), name='Forgot Password OTP'),
    path('forgotpassword/', app.ForgotPasswordView.as_view(), name='Forgot Password'),
    path('profile/', app.Profile.as_view(), name='User Profile'),
    path('userprofile/<str:username>/', app.UserProfile.as_view(), name='Profile'),
    path('deleteaccount/', app.DeleteAccount.as_view(), name='Delete Account'),
    path('changepassword/', app.ChangePassword.as_view(), name='Change Password'),
    path('changeemailotp/', app.ChangeEmailOTP.as_view(), name='Change Email OTP'),
    path('changeemail/', app.ChangeEmail.as_view(), name='Change Email'),
    path('support/', app.Support.as_view(), name='Support'),
    path('patohg-auth/', include('rest_framework.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

APP_NAME = _("پاتوق")
admin.site.site_header = _("پنل مدیریت ") + APP_NAME
admin.site.site_title = APP_NAME
admin.site.index_title = _("پنل مدیریت ")