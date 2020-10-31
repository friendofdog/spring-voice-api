from springapi.models.google.client import (
    create_auth_request as client_get_auth,
    exchange_auth_token as client_get_token)
from springapi.exceptions import AuthorizationError, AuthProviderResponseError


def get_auth_code_uri(redirect_host, credentials):
    try:
        redirect = client_get_auth(redirect_host, credentials)
    except AuthProviderResponseError as e:
        raise AuthorizationError(e)
    return redirect


def exchange_token(params):
    try:
        client_get_token(params)
    except AuthProviderResponseError as e:
        raise AuthorizationError(e)
    return {"success": True}
