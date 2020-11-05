import json
import requests
import urllib

from springapi.exceptions import AuthProviderResponseError, ValidationError
from springapi.helpers import VERSION


def create_auth_request(redirect_host, credentials):
    try:
        client_id = credentials["web"]["client_id"]
    except KeyError:
        raise ValidationError("Bad credentials")
    params = {
        "access_type": "offline",
        "client_id": client_id,
        "redirect_uri": f"{redirect_host}api/{VERSION}/auth-callback",
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/userinfo.email "
                 "https://www.googleapis.com/auth/userinfo.profile "
    }
    oauth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    full_url = f"{oauth_url}?{urllib.parse.urlencode(params)}"
    return full_url


def exchange_auth_token(auth_code, credentials, redirect_host):
    try:
        client_id = credentials["web"]["client_id"]
        client_secret = credentials["web"]["client_secret"]
    except KeyError:
        raise ValidationError("Bad credentials")

    url = "https://oauth2.googleapis.com/token"
    data = {
        "code": auth_code["code"],
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": f"{redirect_host}api/{VERSION}/auth-callback",
        "grant_type": "authorization_code"}
    try:
        response = requests.post(url, data=data)
        token_data = json.loads(response.content)
        assert "access_token" in token_data
    except AssertionError:
        raise AuthProviderResponseError(f"Error retrieving token from {url}")
    return token_data
