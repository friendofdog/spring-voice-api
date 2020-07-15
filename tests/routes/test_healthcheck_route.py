from tests.helpers import test_client
import unittest


class TestHealthCheckHandler(unittest.TestCase):

    def test_healthcheck_returns_200(self):
        with test_client() as client:
            response = client.get("/api/v1/healthcheck")
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual({"success": True}, json)
