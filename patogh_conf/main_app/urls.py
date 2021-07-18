from django.db import router
from django.urls import path
from main_app import views
from django.urls.resolvers import URLPattern
from main_app.views import SignupApiView, SigninApiView, UserInfoApiView
router.register('userprofile',views.UserProfile)
router.register('GatheringList',views.GatheringList)

urlpatterns = [
    path('signup/', SignupApiView.as_view() , name = 'user_signup'),
    path('signin/', SigninApiView.as_view() , name = 'user_signin'),
    path('profile/',UserInfoApiView.as_view(), name = 'user_info' ),
]
urlpatterns += router.urls