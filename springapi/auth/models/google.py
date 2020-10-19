import requests


def request_auth_code(params):
    url = "https://accounts.google.com/o/oauth2/v2/auth"
    try:
        response = requests.get(
            url=url, params=params)
        assert response.status_code == 200
    except AssertionError:
        raise GoogleResponseError(f"Error retrieving auth code from {url}")
    return {"success": True}


def exchange_token(params):
    url = "https://oauth2.googleapis.com/token"
    try:
        response = requests.post(
            url=url, params=params)
        assert response.status_code == 200
    except AssertionError:
        raise GoogleResponseError(f"Error retrieving token from {url}")
    return {"success": True}


class GoogleResponseError(Exception):
    pass
