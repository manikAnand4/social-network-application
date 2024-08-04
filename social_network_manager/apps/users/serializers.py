from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone
from rest_framework import (
    exceptions as rest_exceptions,
    serializers as rest_serializers,
)
from rest_framework.authtoken.models import Token

from apps.users import (
    constants as users_constants,
    models as user_models
)


class LoginSerializer(rest_serializers.Serializer):
    """
    This Serializer class is used to validate the login credentials.
    """

    email = rest_serializers.EmailField(max_length=users_constants.CHAR_FIELD_MAX_LENGTH, write_only=True)
    password = rest_serializers.CharField(max_length=users_constants.CHAR_FIELD_MAX_LENGTH, write_only=True)
    token = rest_serializers.CharField(read_only=True)

    def _authenticate(self, data):
        user = user_models.User.objects.filter(email__iexact=data['email']).first()
        if not (user and user.check_password(data['password'])):
            raise rest_exceptions.AuthenticationFailed()
        
        return user

    def validate(self, data):
        data['user'] = self._authenticate(data)
        
        return data

    def create(self, validated_data):
        user_instance = validated_data['user']
        validated_data['token'], _ = Token.objects.get_or_create(user=user_instance)

        return validated_data


class UserSignUpSerializer(rest_serializers.ModelSerializer):
    """
    This serializer is used to validate users data for signup
    """

    def validate_password(self, password):
        """
        Hash the given password
        """
        return make_password(password)

    class Meta:
        model = user_models.User
        fields = ('email', 'first_name', 'last_name', 'password', 'id')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }


class CreateUpdateFriendRequestSerializer(rest_serializers.ModelSerializer):
    """
    This serializer is used to CReate/Update Friend requests
    """
    recipient_id = rest_serializers.CharField(write_only=True, required=False)
    status = rest_serializers.ChoiceField(
        write_only=True, required=False,
        choices=list(user_models.FriendRequest.STATUS_NAME_DICT.keys())
    )
    request_id = rest_serializers.IntegerField(read_only=True, source='id')

    class Meta:
        model = user_models.FriendRequest
        fields = ('recipient_id', 'request_id', 'status')

    def validate_recipient_id(self, id):
        # check if id is valid db id or not. 
        if not user_models.User.objects.filter(id=id).exists():
            raise rest_exceptions.ValidationError(users_constants.ERROR_MESSAGES['INVALID_RECIPIENT'])
        
        return id

    def validate(self, attrs):
        # Create Request validations
        if self.context['request'].method == 'POST':
            # check if recipient id is present or not
            if not attrs.get('recipient_id'):
                raise rest_exceptions.ValidationError(users_constants.ERROR_MESSAGES['MISSING_RECIPIENT_ID'])
            
            # check if user has exceeded 1 minute quota
            one_minute_ago = timezone.now() - timedelta(minutes=1)
            user_requests = user_models.FriendRequest.objects.filter(
                sender_id=self.context['request'].user.id,
                status=user_models.FriendRequest.STATUS_PENDING,
                created_at__gte=one_minute_ago
            ).count()
            if user_requests >= users_constants.FRIEND_REQUEST_QUOTA:
                raise rest_exceptions.ValidationError(users_constants.ERROR_MESSAGES['FRIEND_REQUEST_QUOTA_EXCEED'])

            existing_request = user_models.FriendRequest.objects.filter(
                sender_id=self.context['request'].user.id, recipient_id=attrs['recipient_id']
            ).first()

            # check if user is already a friend with the recipient.
            if existing_request and existing_request.status == user_models.FriendRequest.STATUS_ACCEPTED:
                raise rest_exceptions.ValidationError(users_constants.ERROR_MESSAGES['ALREADY_FRIEND'])

            # check if friend request is already in a peding status
            if existing_request and existing_request.status == user_models.FriendRequest.STATUS_PENDING:
                raise rest_exceptions.ValidationError(users_constants.ERROR_MESSAGES['ALREADY_SENT'])

            if existing_request:
                attrs['existing_request'] = existing_request
        else:
            # check if status is present or not
            if not attrs.get('status'):
                raise rest_exceptions.ValidationError(users_constants.ERROR_MESSAGES['MISSING_STATUS'])
        
        return super().validate(attrs)

    @transaction.atomic()
    def create(self, validated_data):
        friend_request = None
        # Update status of existing request
        if validated_data.get('existing_request'):
            friend_request = validated_data.get('existing_request')
            friend_request.status = user_models.FriendRequest.STATUS_PENDING
            friend_request.save(update_fields=['status'])
        # create new request
        else:
            validated_data['sender_id'] = self.context['request'].user.id
            validated_data['status'] = user_models.FriendRequest.STATUS_PENDING
            friend_request = super().create(validated_data)

        return friend_request

    @transaction.atomic
    def update(self, instance, validated_data):
        # check if the request is in pending state or not
        if instance.status != user_models.FriendRequest.STATUS_PENDING:
            raise rest_exceptions.ValidationError(users_constants.ERROR_MESSAGES['ALREADY_PROCESSED_REQUEST'])

        # create a user network if request is accepted
        if validated_data['status'] == user_models.FriendRequest.STATUS_ACCEPTED:
            user_models.UserNetwork.objects.get_or_create(
                user_id=self.context['request'].user.id, friend_id=instance.sender_id
            )

        return super().update(instance, validated_data)


class GetPendingRequestSerializer(rest_serializers.ModelSerializer):
    """
    This serializer is used to prepare response for pending requests for a user
    """
    sender_email = rest_serializers.CharField(source='sender.email')
    sender_name = rest_serializers.CharField(source='sender.full_name')

    class Meta:
        model = user_models.FriendRequest
        fields = ('id', 'sender_email', 'sender_name')


class GetUserFriendsSerializer(rest_serializers.ModelSerializer):
    """
    This serializer is used to prepare response for  users friends
    """
    friend_email = rest_serializers.CharField(source='friend.email')
    friend_name = rest_serializers.CharField(source='friend.full_name')

    class Meta:
        model = user_models.UserNetwork
        fields = ('id', 'friend_email', 'friend_name')
