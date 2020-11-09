from springapi.models.google.client import (
    create_auth_request as client_get_auth,
    exchange_auth_token as client_get_token,
    get_authenticated_user as client_get_user)
from springapi.models.email import Email
from springapi.exceptions import (
    AuthorizationError, AuthProviderResponseError, ValidationError)


def get_auth_code_uri(redirect_host, credentials):
    try:
        redirect = client_get_auth(redirect_host, credentials)
    except AuthProviderResponseError as e:
        raise AuthorizationError(e)
    return redirect


def validate_user(token):
    valid_emails = Email.get_authorized_emails()
    user = client_get_user(token)
    user_email = user["email"]
    try:
        assert user_email in valid_emails
    except AssertionError:
        raise ValidationError(user_email)


def exchange_oauth_token(auth_code, credentials, redirect_host):
    try:
        token = client_get_token(auth_code, credentials, redirect_host)
    except AuthProviderResponseError as e:
        raise AuthorizationError(e)
    try:
        validate_user(token)
    except ValidationError as e:
        raise AuthorizationError(
            f"User associated with {e} is not authorized")
    return token
