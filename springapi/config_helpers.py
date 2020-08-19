import base64
import binascii
import json
import urllib


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


class InvalidJSONURI(Exception):
    pass
