import json
import requests
import urllib

from springapi.exceptions import AuthProviderResponseError
from springapi.config_helpers import VERSION


def create_auth_request_uri(
        redirect_host, client_id,
        oauth_url="https://accounts.google.com/o/oauth2/v2/auth"):

    params = {
        "access_type": "offline",
        "client_id": client_id,
        "redirect_uri": f"{redirect_host}api/{VERSION}/auth-callback",
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/userinfo.email "
                 "https://www.googleapis.com/auth/userinfo.profile "
    }

    full_url = f"{oauth_url}?{urllib.parse.urlencode(params)}"
    return full_url


def get_oauth_token(
        auth_code, credentials, redirect_host,
        token_url="https://oauth2.googleapis.com/token"):
    client_id = credentials["web"]["client_id"]
    client_secret = credentials["web"]["client_secret"]

    data = {
        "code": auth_code["code"],
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": f"{redirect_host}api/{VERSION}/auth-callback",
        "grant_type": "authorization_code"}

    response = requests.post(token_url, data=data)
    token_data = json.loads(response.content)

    if "access_token" not in token_data:
        raise AuthProviderResponseError(
            f"Error retrieving token from {token_url}")
    return token_data["access_token"]


def get_authenticated_user_email(
        token, user_url="https://www.googleapis.com/oauth2/v2/userinfo"):
    full_url = f"{user_url}?access_token={token}"
    try:
        response = requests.get(full_url)
        user_data = json.loads(response.content)
        assert "email" in user_data
    except AssertionError:
        raise AuthProviderResponseError(
            f"Error retrieving user info from {user_url}")
    return user_data["email"]
