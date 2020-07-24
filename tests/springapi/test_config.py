import unittest
from unittest import mock

from springapi.config import Configuration


class TestConfiguration(unittest.TestCase):

    def test_configuration_allows_firebase_value(self):
        mock_firebase = mock.Mock()
        config = Configuration(firebase=mock_firebase)
        self.assertEqual(config.firebase, mock_firebase)
