import requests
from requests.adapters import HTTPAdapter

URL = "http://localhost:8081"
PARAMS = {
    "client_id": 1234,
    "redirect_uri": "http://localhost:5000/api/v1/auth",
    "response_type": "code",
    "scope": "https://www.googleapis.com/auth/drive.metadata.readonly"
}


def google_request_auth_token():
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=5)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.get(url=f"{URL}/mock-auth", params=PARAMS)
