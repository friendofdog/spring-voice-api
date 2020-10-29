import unittest
from springapi.models.user import User
from unittest import mock


@mock.patch('springapi.models.firebase.client.get_collection')
class TestUsers(unittest.TestCase):

    def __init__(self, _):
        super().__init__(_)
        self.entries = {
            "abc": {
                "email": "foo@bar",
                "isAdmin": True,
                "token": "123"
            },
            "def": {
                "token": "i am missing a required field"
            },
            "ghi": {
                "email": "hi@low",
                "isAdmin": True,
                "token": "456"
            },
            "jkl": {
                "email": "hussle@bustle",
                "isAdmin": False,
                "token": "789"
            }
        }
        self.valid = [
            self.entries["abc"], self.entries["ghi"], self.entries["jkl"]
        ]

    def test_get_users_returns_list_of_users(self, mock_get):
        mock_get.return_value = self.entries
        users = User.get_users()
        self.assertEqual(self.valid, [u.to_json() for u in users])
        mock_get.assert_called_with("users", None, None)

    def test_get_users_omits_invalid_entries(self, mock_get):
        mock_get.return_value = self.entries
        users = User.get_users()
        self.assertNotIn(self.entries["def"], [u.to_json() for u in users])
        mock_get.assert_called_with("users", None, None)

    def test_get_users_given_field_value_returns_list_of_users(self, mock_get):
        mock_get.return_value = {"jkl": self.entries["jkl"]}
        users = User.get_users('token', '789')
        self.assertEqual([self.entries["jkl"]], [u.to_json() for u in users])
        mock_get.assert_called_with("users", "token", "789")
