import requests
import urllib

from springapi.exceptions import AuthProviderResponseError


def create_auth_request(redirect_host, credentials):
    try:
        client_id = credentials["client_id"]
    except KeyError:
        raise AuthProviderResponseError("Bad credentials")
    params = {
        "client_id": client_id,
        "redirect_uri": f"{redirect_host}api/v1/auth-callback",
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/userinfo.email "
                 "https://www.googleapis.com/auth/userinfo.profile "
    }
    oauth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    full_url = f"{oauth_url}?{urllib.parse.urlencode(params)}"
    return full_url


def exchange_auth_token(params):
    url = "https://oauth2.googleapis.com/token"
    try:
        response = requests.post(url=url, params=params)
        assert response.status_code == 200
    except AssertionError:
        raise AuthProviderResponseError(f"Error retrieving token from {url}")
    return {"success": True}
