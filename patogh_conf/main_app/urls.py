
from django.urls import path
import views
from django.urls.resolvers import URLPattern
from .views import SignupApiView, SigninApiView, UserInfoApiView , SearchDorehami

urlpatterns = [
    path('signup/', SignupApiView.as_view() , name = 'user_signup'),
    path('signin/', SigninApiView.as_view() , name = 'user_signin'),
    path('profile/',UserInfoApiView.as_view(), name = 'user_info' ),
    path('searchGatherings/', views.SearchDorehami),
    path('addGathering/', views.AddDorehami),
path('userprofile/', views.UserProfile)
]