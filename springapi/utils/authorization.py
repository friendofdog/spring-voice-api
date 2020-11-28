import jwt

from springapi.utils.google.client import (
    create_auth_request_uri, get_oauth_token, get_authenticated_user_email)
from springapi.models.email import Email
from springapi.models.token import Token
from springapi.exceptions import (
    AuthorizationError, AuthProviderResponseError, ValidationError)


def get_auth_code_uri(redirect_host, client_id):
    return create_auth_request_uri(redirect_host, client_id)


def _validate_user_by_email(token):
    valid_emails = Email.get_authorized_emails()
    user_email = get_authenticated_user_email(token)
    if user_email not in valid_emails:
        raise ValidationError(user_email)
    return user_email


def exchange_oauth_token(auth_code, credentials, redirect_host):
    try:
        token = get_oauth_token(auth_code, credentials, redirect_host)
    except AuthProviderResponseError as e:
        raise AuthorizationError(e)
    try:
        email = _validate_user_by_email(token)
    except ValidationError as e:
        raise AuthorizationError(
            f"User associated with {e} is not authorized")
    return email


def generate_api_token(email, key):
    payload = {
        "email": email,
        "iss": "springapi"
    }
    token = jwt.encode(payload, key, algorithm="HS256")
    return token


def create_api_token(auth_code, credentials, key, redirect_host):
    email = exchange_oauth_token(auth_code, credentials, redirect_host)
    api_token = generate_api_token(email, key)
    token_obj = {"token": api_token.decode("utf-8")}
    Token.create_token(token_obj)
    return api_token
