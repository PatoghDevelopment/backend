from django.urls import path
from .views import *

urlpatterns = [
    # athentication paths
    path('get_otp', SingUpSendOTP.as_view(), name='user_signup'),
    path('signup/', Signup.as_view(), name='signup'),
    path('signin/', Signin.as_view(), name='signin'),
    path('forgotpasswordotp/', ForgotPasswordSendOTP.as_view(), name='forgot-password_otp'),
    path('forgotpassword/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('profile/', Profile.as_view(), name='User Profile'),
    path('userprofile/<str:email>/', UserProfile.as_view(), name='Profile'),
    path('deleteaccount/', DeleteAccount.as_view(), name='Delete Account'),
    path('changepassword/', ChangePassword.as_view(), name='Change Password'),
    path('support/', Support.as_view(), name='Support'),


    # Patogh paths
    #path('patogh/detail/<uuid:pk>/', PatoghDetail.as_view(), name="patogh_detail"),
    #path('patogh/detail/limit/<uuid:pk>/', PatoghDetailLimitedColumn.as_view(), name="patogh_detail_limited_column"),
    #path('patogh/create/', PatoghCreateAndUpdateAndDelete.as_view(), name='patoghCreate'),
    #path('patogh/update/', PatoghCreateAndUpdateAndDelete.as_view(), name='patoghUpdate'),
    #path('patogh/delete/', PatoghCreateAndUpdateAndDelete.as_view(), name='patoghDelete'),
    path('newfriendrequest/<str:username>', FriendRequestListCreate.as_view()),
    path('friendrequests/', FriendRequestListCreate.as_view()),
    path('acceptfriendrequest/<str:username>', AcceptFriendRequest.as_view()),
    path('removefriendrequest/<str:username>', RemoveFriendRequest.as_view()),
    path('friends/', FriendList.as_view()),
    path('removefriend/<str:username>/', RemoveFriend.as_view()),
    # path('patogh/list/', PatoghDetailWithSearch.as_view(), name="patogh_list_with_search"),

    # users parties
    path('parties/', UserParties.as_view(), name="user_parties"),
]
