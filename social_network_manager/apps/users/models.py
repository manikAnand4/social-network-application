from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users import constants as user_constants
from apps.commons import models as commons_models

class User(AbstractUser, commons_models.DatesModel):
    """
    Overridden the user model to make username nullable and create indexes for faster searching.
    """

    email = models.EmailField(
        help_text=user_constants.HELP_TEXT['EMAIL'],
        max_length=user_constants.CHAR_FIELD_MAX_LENGTH,
        unique=True,
    )
    username = models.CharField(
        help_text=user_constants.HELP_TEXT['USERNAME'],
        max_length=user_constants.CHAR_FIELD_MAX_LENGTH,
        unique=True, null=True, blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['email'])
        ]
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}' if self.last_name else self.first_name

    def __str__(self) -> str:
        return f'{self.email} - {self.username}'


class FriendRequest(commons_models.DatesModel):
    """
    Model to store friend requsts of a user.
    Fields:
        sender: user's fk who is sending the friend request
        recipient: user's fk who is recieving the friend request
        status: int field depicting the current status of the request
    """

    STATUS_ACCEPTED, STATUS_REJECTED, STATUS_PENDING = range(1, 4)
    STATUS_CHOICES = (
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_PENDING, 'Pending'),
    )
    STATUS_NAME_DICT = dict(STATUS_CHOICES)

    sender = models.ForeignKey(
        to=User,
        help_text=user_constants.HELP_TEXT['REQUEST_SENDER'],
        on_delete=models.CASCADE,
        related_name='sent_requests'
    )
    recipient = models.ForeignKey(
        to=User,
        help_text=user_constants.HELP_TEXT['REQUEST_APPROVAR'],
        on_delete=models.CASCADE,
        related_name='recieved_requests'
    )
    status = models.IntegerField(choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('sender_id', 'recipient_id')

    def __str__(self) -> str:
        return f'{self.sender.email} - {self.recipient.email} - {self.STATUS_NAME_DICT[self.status]}'


class UserNetwork(commons_models.DatesModel):
    """
    Model to store a users network i.e friends.
    Fields:
        user: User whose network is being referred
        user_friend: User whose friend is being referred
    """

    user = models.ForeignKey(
        to=User,
        help_text=user_constants.HELP_TEXT['USERNETWORK_USER'],
        related_name='followers',
        on_delete=models.CASCADE,
    )
    friend = models.ForeignKey(
        to=User,
        help_text=user_constants.HELP_TEXT['USERNETWORK_FRIEND'],
        related_name='followings',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('user_id', 'friend_id')

    def __str__(self) -> str:
        return f'{self.user.email} - {self.friend.email}'
