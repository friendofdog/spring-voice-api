import requests


def request_auth_code(params=None):
    if params is None:
        params = {
            "client_id": "abcde",
            "redirect_uri": "http://localhost:5000/api/v1/auth",
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/userinfo.email "
                     "https://www.googleapis.com/auth/userinfo.profile "
                     "openid"
        }
    requests.get(
        url="http://localhost:8081/mock-auth", params=params)
    return {"success": True}


def exchange_auth_token(params=None):
    if params is None:
        params = {
            "code": "54321",
            "client_id": "abcde",
            "client_secret": "qwerty",
            "redirect_uri": "http://localhost:5000/api/v1/auth-callback",
            "grant_type": "authorization_code"
        }
    requests.post(
        url="http://localhost:8081/mock-token", params=params)
    return {"success": True}
