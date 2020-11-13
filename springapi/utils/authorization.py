from springapi.utils.google.client import (
    create_auth_request_uri, get_oauth_token, get_authenticated_user)
from springapi.models.email import Email
from springapi.exceptions import (
    AuthorizationError, AuthProviderResponseError, ValidationError)


def get_auth_code_uri(redirect_host, client_id):
    return create_auth_request_uri(redirect_host, client_id)


def validate_user(token):
    valid_emails = Email.get_authorized_emails()
    user = get_authenticated_user(token)
    user_email = user["email"]
    if user_email not in valid_emails:
        raise ValidationError(user_email)


def exchange_token(auth_code, credentials, redirect_host):
    try:
        token = get_oauth_token(auth_code, credentials, redirect_host)
    except AuthProviderResponseError as e:
        raise AuthorizationError(e)
    try:
        validate_user(token)
    except ValidationError as e:
        raise AuthorizationError(
            f"User associated with {e} is not authorized")
    return token
