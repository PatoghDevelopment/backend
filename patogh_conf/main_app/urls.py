from django.urls import path
from .views import *

urlpatterns = [
    # athentication paths

    # Patogh paths
    # path('patogh/detail/<uuid:pk>/', PatoghDetail.as_view(), name="patogh_detail"),
    # path('patogh/detail/limit/<uuid:pk>/', PatoghDetailLimitedColumn.as_view(), name="patogh_detail_limited_column"),
    # path('patogh/create/', PatoghCreateAndUpdateAndDelete.as_view(), name='patoghCreate'),
    # path('patogh/update/', PatoghCreateAndUpdateAndDelete.as_view(), name='patoghUpdate'),
    # path('patogh/delete/', PatoghCreateAndUpdateAndDelete.as_view(), name='patoghDelete'),
    # path('patogh/list/', PatoghDetailWithSearch.as_view(), name="patogh_list_with_search"),

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
    path('newhangout/', HangoutCreate.as_view()),
    path('allhangouts/', HangoutList.as_view()),
    path('hangout/<int:pk>/members/', HangoutMembers.as_view()),
    path('finishhangout/<int:pk>/', FinishHangout.as_view()),
    path('followinghangouts/', FollowingHangoutsList.as_view()),
    path('finishedhangouts/', FinishedHangouts.as_view()),
    path('invitetohangout/<int:pk>/<str:username>/', InviteHangoutMember.as_view()),
    path('hangoutinvitations/', HangoutInvitations.as_view()),
    path('accepthangoutinvitation/<int:pk>/', AcceptHangoutInvitation.as_view()),
    path('rejecthangoutinvitation/<int:pk>/', RejectHangoutInvitation.as_view()),
    path('hangout-rud/<int:pk>/', HangoutRUD.as_view()),
    path('leavehangout/<int:pk>/', LeaveHangout.as_view()),
    path('hangout/<int:pk>/removemember/<str:username>/', )



]
