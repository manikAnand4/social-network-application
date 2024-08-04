from django.urls import path
from apps.users import views as users_views


urlpatterns = [
    path('login/', users_views.LoginAPIView.as_view(), name='login'),
    path('sign-up/', users_views.UserSignUpAPIView.as_view(), name='sign-up'),
    path('users-list/', users_views.GetUsersListAPIView.as_view(), name='users-list'),
    path('friend-request/', users_views.CreateFriendRequestAPIView.as_view({'post': 'create'}), name='add-friend-request'),
    path('friend-request/<int:pk>', users_views.CreateFriendRequestAPIView.as_view({'patch': 'partial_update'}), name='update-friend-request'),
    path('pending-requests/', users_views.GetPendingRequestsAPIView.as_view(), name='pending-requests'),
    path('user-friends/', users_views.GetUserFriendsAPIView.as_view(), name='user-friends'),
]
