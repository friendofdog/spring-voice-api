import base64
import binascii
import json
import urllib.parse


AUTH = "AUTH"
CLIENT_ID = "CLIENT_ID"
SUBMISSION = "SUBMISSION"
TOKEN = "TOKEN"
USER = "USER"
VERSION = "v1"


def encode_json_uri(scheme, config):
    json_config = json.dumps(config).encode("utf8")
    base64_config = base64.urlsafe_b64encode(json_config).decode("utf8")
    return f"{scheme}://{base64_config}"


def decode_json_uri(uri):
    parsed_url = urllib.parse.urlparse(uri)
    try:
        base64_config = base64.b64decode(parsed_url.netloc)
    except binascii.Error:
        raise InvalidJSONURI("The config URI provided is not base64 encoded.")
    try:
        config = json.loads(base64_config)
    except json.JSONDecodeError:
        raise InvalidJSONURI("The config URI provided is not valid JSON.")
    return parsed_url.scheme, config


def _verify_auth_credentials(config):
    auth_uri = config[AUTH]
    scheme, credentials = decode_json_uri(auth_uri)

    if scheme == "google":
        pass
    else:
        raise ValueError(f"Unknown authorization protocol: {scheme}")

    return credentials


def create_config(environ):
    config = {}
    config["ENV"] = environ.get("FLASK_ENV", "testing")
    config["DEBUG"] = config["ENV"] == "development"

    assert AUTH in environ
    assert USER in environ
    assert TOKEN in environ

    auth_credentials = _verify_auth_credentials(environ)
    config[AUTH] = auth_credentials
    config[USER] = environ[USER]
    config[TOKEN] = environ[TOKEN]

    assert "web" in config[AUTH]
    assert "client_id" in config[AUTH]["web"]

    config[CLIENT_ID] = config[AUTH]["web"]["client_id"]
    return config


class InvalidJSONURI(Exception):
    pass
