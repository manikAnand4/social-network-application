from django.db.models import Q, F
from django.utils.text import smart_split
from rest_framework import (
    generics,
    mixins as rest_mixins,
    viewsets as rest_viewsets,
)
from rest_framework.permissions import AllowAny

from apps.users import (
    models as users_models,
    permissions as users_permissions,
    serializers as users_serializers,
)


class LoginAPIView(generics.CreateAPIView):
    """
    API to handle user's login
    Body:
        email: email of the user
        password: password of the user
    Response:
        token: token of the user if login successful.
    """
    permission_classes = [AllowAny,]
    serializer_class = users_serializers.LoginSerializer


class UserSignUpAPIView(generics.CreateAPIView):
    """
    API to handle user's Signup
    Body:
        email: email of the user
        first_name: first name of the user (Optional)
        last_name: last name of the user (Optional)
        passowrd: password of the user
    Response:
        email: email of the user
        first_name: first name of the user
        last_name: last name of the user
    """
    permission_classes = [AllowAny,]
    serializer_class = users_serializers.UserSignUpSerializer


class GetUsersListAPIView(generics.ListAPIView):
    """
    API to return user list
    QueryParams:
        search: search text to be searched
    Response(Paginated i.e inside a response key):
        email: email of the user
        first_name: first name of the user
        last_name: last name of the user
    """
    serializer_class = users_serializers.UserSignUpSerializer
    SEARCH_KEYWORD = 'search'
    DEFAULT_ORDERING = 'created_at'

    def get_queryset(self):
        qs = users_models.User.objects.exclude(id=self.request.user.id).order_by(self.DEFAULT_ORDERING)
        search_text = self.request.GET.get(self.SEARCH_KEYWORD)
        # search text could be an email or space separated name
        # eg -> 'manik@gmail.com' or 'manik' or 'manik anand'
        search_text_list = smart_split(search_text)
        search_query = None
        
        if search_text:
            # Case when we have manikanand2@gmail.com. Exact match is required
            search_query = Q(email=search_text)
            # Case 'manik' or 'manik anand'
            for search in search_text_list:
                search_query = search_query | Q(first_name__icontains=search) | Q(last_name__icontains=search)

        return qs.filter(search_query) if search_query else qs


class CreateFriendRequestAPIView(
    rest_mixins.CreateModelMixin,
    rest_mixins.UpdateModelMixin,
    rest_viewsets.GenericViewSet
):
    """
    API to create friend request.
    Body:
        recipient_id: id of the recipient
        status: status of request while accepting/rejecting
    Response:
        request_id: id of the request
    """
    permission_classes = (users_permissions.HasFriendRequestCreateUpdatePermission,)
    serializer_class = users_serializers.CreateUpdateFriendRequestSerializer
    queryset = users_models.FriendRequest.objects.all()


class GetPendingRequestsAPIView(generics.ListAPIView):
    """
    API to create friend request.
    Response:
        Paginated response with list of pending requests
    """
    serializer_class = users_serializers.GetPendingRequestSerializer
    
    def get_queryset(self):
        return users_models.FriendRequest.objects.filter(
            recipient=self.request.user.id, status=users_models.FriendRequest.STATUS_PENDING
        ).select_related('sender')


class GetUserFriendsAPIView(generics.ListAPIView):
    """
    API to create friend request.
    Response:
        Paginated response with list of user friends
    """
    serializer_class = users_serializers.GetUserFriendsSerializer
    
    def get_queryset(self):
        return users_models.UserNetwork.objects.filter(
            user_id=self.request.user.id
        ).select_related('friend')
