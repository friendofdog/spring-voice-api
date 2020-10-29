import unittest
from springapi.models.user import User
from unittest import mock


@mock.patch('springapi.models.firebase.client.get_collection')
class TestUsers(unittest.TestCase):

    def test_get_users_returns_list_of_found_users(self, mock_get):
        expected = mock_get.return_value = {
            "abc": {
                "email": "foo@bar"
            }
        }
        users = User.get_users()
        self.assertEqual([expected["abc"]], [u.to_json() for u in users])
        mock_get.assert_called_with("users")

    def test_get_users_omits_invalid_entries(self, mock_get):
        expected = mock_get.return_value = {
            "1": {
                "email": "foo@bar"
            },
            "2": {
                "token": "123abc"
            }
        }
        users = User.get_users()
        self.assertEqual([expected["1"]], [u.to_json() for u in users])
        mock_get.assert_called_with("users")
