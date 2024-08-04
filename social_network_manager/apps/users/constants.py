HELP_TEXT = {
    'EMAIL': 'Email of the user',
    'USERNAME': 'Username of the user',
    'REQUEST_SENDER': 'User sending the friend request',
    'REQUEST_APPROVAR': 'User recieving the friend request',
    'USERNETWORK_USER': 'User whose friends we are storing',
    'USERNETWORK_FRIEND': 'User who is added as a friend', 
}

CHAR_FIELD_MAX_LENGTH = 150
FRIEND_REQUEST_QUOTA = 3

ERROR_MESSAGES = {
    'ALREADY_FRIEND': 'This user is already your friend.',
    'ALREADY_SENT': 'Friend request has already been sent.',
    'FRIEND_REQUEST_QUOTA_EXCEED': f'You can only send {FRIEND_REQUEST_QUOTA} requests in 1 min.',
    'INVALID_RECIPIENT': 'Please provide a valid recipient.',
    'MISSING_RECIPIENT_ID': 'Please provide recipient id for friend request creation.',
    'INVALID_VALID_STATUS': 'Provide a valid status',
    'MISSING_STATUS': 'Please provide a status.',
    'ALREADY_PROCESSED_REQUEST': 'This request is already accepted/rejected.'
}

