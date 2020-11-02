import json
import requests
import urllib

from springapi.exceptions import AuthProviderResponseError, ValidationError


def create_auth_request(redirect_host, credentials):
    try:
        client_id = credentials["client_id"]
    except KeyError:
        raise ValidationError("Bad credentials")
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


def exchange_auth_token(redirect_host, credentials, auth_code):
    try:
        client_id = credentials["client_id"]
        client_secret = credentials["client_secret"]
    except KeyError:
        raise ValidationError("Bad credentials")
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    url = "https://oauth2.googleapis.com/token"
    body = {
        "code": auth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_host,
        "grant_type": "authorization_code"
    }
    try:
        response = requests.post(url=url, headers=headers, body=body)
        token_data = json.loads(response.content)
        assert "access_token" in token_data
    except AssertionError:
        raise AuthProviderResponseError(f"Error retrieving token from {url}")
    return token_data
