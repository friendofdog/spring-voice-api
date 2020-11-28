import base64
import json
import unittest
import urllib

from springapi.helpers import decode_json_uri, encode_json_uri
from springapi.exceptions import InvalidJSONURI


class TestConfigHelpers(unittest.TestCase):

    def test_encode_json_uri_uses_base64_for_values(self):
        config = {"username": "FOOBAR", "password": "PASSWORD"}
        scheme = "firestore"
        result = encode_json_uri(scheme, config)

        parsed_url = urllib.parse.urlparse(result)
        self.assertEqual(scheme, parsed_url.scheme)
        result_config = json.loads(base64.b64decode(parsed_url.netloc))
        self.assertEqual(config, result_config)

    def test_encode_json_uri_supports_variable_schemes(self):
        config = {"host": "localhost", "db": "admin"}
        scheme = "mysql"
        result = encode_json_uri(scheme, config)

        parsed_url = urllib.parse.urlparse(result)
        self.assertEqual(scheme, parsed_url.scheme)
        result_config = json.loads(base64.b64decode(parsed_url.netloc))
        self.assertEqual(config, result_config)

    def test_decode_json_uri_returns_scheme_and_configuration(self):
        config = {"username": "FOOBAR", "password": "PASSWORD"}
        scheme = "mysql"
        uri = encode_json_uri(scheme, config)

        result_scheme, result_config = decode_json_uri(uri)
        self.assertEqual(scheme, result_scheme)
        self.assertEqual(config, result_config)

    def test_decode_json_uri_raises_helpful_warning_with_invalid_json(self):
        invalid_json = base64.urlsafe_b64encode("INVALID_JSON".encode("utf8"))
        uri = f"scheme://{invalid_json.decode('utf8')}"

        with self.assertRaises(InvalidJSONURI):
            decode_json_uri(uri)

    def test_decode_json_uri_raises_helpful_warning_with_invalid_base64(self):
        uri = "scheme://INVALID_JSON"

        with self.assertRaises(InvalidJSONURI):
            decode_json_uri(uri)
