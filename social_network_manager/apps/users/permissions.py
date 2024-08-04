from rest_framework.permissions import BasePermission

from apps.users import models as users_models

class HasFriendRequestCreateUpdatePermission(BasePermission):
    """
    Permission class to check if user can Accept/Reject friend request.
    """

    def has_permission(self, request, view):
        # check if user is a recipient of that request or not.
        return  users_models.FriendRequest.objects.filter(
            recipient_id=request.user.id, id=view.kwargs.get('pk')
        ).exists() if request.method == 'PATCH' else True        
