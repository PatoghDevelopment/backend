from django.urls import path
from .views import *

urlpatterns = [
    # athentication paths
    path('signupotp/', SignupSendOTP.as_view(), name='Signup OTP'),
    path('signup/', Signup.as_view(), name='Signup'),
    path('signin/', Signin.as_view(), name='Signin'),
    path('forgotpasswordotp/', ForgotPasswordSendOTP.as_view(), name='Forgot Password OTP'),
    path('forgotpassword/', ForgotPasswordView.as_view(), name='Forgot Password'),
    path('profile/', Profile.as_view(), name='User Profile'),
    path('userprofile/<str:username>/', UserProfile.as_view(), name='Profile'),
    path('deleteaccount/', DeleteAccount.as_view(), name='Delete Account'),
    path('changepassword/', ChangePassword.as_view(), name='Change Password'),
    path('support/', Support.as_view(), name='Support'),


    # Patogh paths
    #path('patogh/detail/<uuid:pk>/', PatoghDetail.as_view(), name="patogh_detail"),
    #path('patogh/detail/limit/<uuid:pk>/', PatoghDetailLimitedColumn.as_view(), name="patogh_detail_limited_column"),
    #path('patogh/create/', PatoghCreateAndUpdateAndDelete.as_view(), name='patoghCreate'),
    #path('patogh/update/', PatoghCreateAndUpdateAndDelete.as_view(), name='patoghUpdate'),
    #path('patogh/delete/', PatoghCreateAndUpdateAndDelete.as_view(), name='patoghDelete'),
    #path('patogh/list/', PatoghDetailWithSearch.as_view(), name="patogh_list_with_search"),

    path('newfriendrequest/<str:username>', FriendRequestListCreate.as_view()),
    path('friendrequests/', FriendRequestListCreate.as_view()),
    path('acceptfriendrequest/<str:username>/', AcceptFriendRequest.as_view()),
    path('removefriendrequest/<str:username>/', RemoveFriendRequest.as_view()),
    path('friends/', FriendList.as_view()),
    path('removefriend/<str:username>/', RemoveFriend.as_view()),
    path('searchuser/<str:username>/', SearchUser.as_view()),
    path('newcompany/', CompanyCreate.as_view()),
    path('companies/', CompanyList.as_view()),
    path('company/<int:pk>/addmember/<str:username>/', AddCompanyMember.as_view()),
    path('company/<int:pk>/leave/', LeaveCompany.as_view()),
    path('company/<int:pk>/removemember/<str:username>/', RemoveMember.as_view()),
    path('company/<int:pk>/members/', CompanyMembers.as_view()),
    path('company-rud/<int:pk>/', CompanyRUD.as_view()),
    path('searchcompany/<str:name>/', CompanySearch.as_view()),
]
