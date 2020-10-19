from springapi.auth.models.google import (
    request_auth_code as client_get_auth,
    exchange_token as client_get_token)


def get_auth_code(params):
    try:
        response = client_get_auth(params)
        assert response == {"success": True}, response
    except AssertionError as e:
        raise AuthorizationError(
            f"Something went wrong with authorization: {e}")
    return {"success": True}


def exchange_token(params):
    try:
        response = client_get_token(params)
        assert response == {"success": True}, response
    except AssertionError as e:
        raise AuthorizationError(
            f"Something went wrong with token exchange: {e}")
    return {"success": True}


class AuthorizationError(Exception):
    pass
