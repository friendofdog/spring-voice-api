import requests
from requests.adapters import HTTPAdapter

URL = "http://localhost:8081"
PARAMS = {
    "client_id": "abcde",
    "redirect_uri": "http://localhost:5000/api/v1/auth",
    "response_type": "code",
    "scope": "https://www.googleapis.com/auth/userinfo.email "
             "https://www.googleapis.com/auth/userinfo.profile "
             "openid"
}


def google_request_auth_code():
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=5)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    code = session.get(url=f"{URL}/mock-auth", params=PARAMS)
    return code


def google_exchange_token(code):
    pass
