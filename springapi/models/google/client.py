import requests
from springapi.exceptions import AuthProviderResponseError


def request_auth_code(credentials):
    user_id = credentials["client_id"]
    params = {
        "client_id": user_id,
        "redirect_uri": "http://localhost:5000/api/v1/auth-callback",
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/userinfo.email "
                 "https://www.googleapis.com/auth/userinfo.profile "
                 "openid"
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth"
    try:
        response = requests.get(url=url, params=params)
        assert response.status_code == 200
    except AssertionError:
        raise AuthProviderResponseError(
            f"Error retrieving auth code from {url}")
    return {"success": True}


def exchange_auth_token(params):
    url = "https://oauth2.googleapis.com/token"
    try:
        response = requests.post(url=url, params=params)
        assert response.status_code == 200
    except AssertionError:
        raise AuthProviderResponseError(f"Error retrieving token from {url}")
    return {"success": True}
