from springapi.auth.models.google import (
    request_auth_code as client_get_auth,
    exchange_auth_token as client_get_token)
from springapi.exceptions import AuthorizationError, AuthProviderResponseError


def get_auth_code(params):
    try:
        client_get_auth(params)
    except AuthProviderResponseError as e:
        raise AuthorizationError(e)
    return {"success": True}


def exchange_token(params):
    try:
        client_get_token(params)
    except AuthProviderResponseError as e:
        raise AuthorizationError(e)
    return {"success": True}
