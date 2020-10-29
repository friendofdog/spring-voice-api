import unittest
from springapi.models.user import User
from springapi.exceptions import EntryNotFound, ValidationError
from unittest import mock


@mock.patch('springapi.models.firebase.client.get_collection')
class TestUserGetUsers(unittest.TestCase):

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
            },
            "mno": {
                "email": "koki@koko",
                "isAdmin": False,
                "token": "789",
                "badField": "should not be here"
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


class TestUserUpdateUser(unittest.TestCase):

    @mock.patch('springapi.models.firebase.client.update_entry')
    def test_update_user_returns_success_if_found_and_valid(self, mocked):
        entry_id = "pqr"
        data = {"email": "dot@com", "isAdmin": False, "token": "357"}
        expected = mocked.return_value = {'success': f'{entry_id} updated'}
        self.assertEqual(expected, User.update_user(entry_id, data))
        mocked.assert_called_with("users", data, entry_id)

    @mock.patch('springapi.models.firebase.client.update_entry')
    def test_update_user_raises_EntryNotFound(self, mock_update):
        entry_id = "pqr"
        err = mock_update.side_effect = EntryNotFound(entry_id, "users")
        data = {"email": "dot@com", "isAdmin": False, "token": "357"}
        with self.assertRaises(EntryNotFound) as context:
            User.update_user(entry_id, data)
        expected = context.exception.error_response_body()
        self.assertEqual(expected, err.error_response_body())

    def test_update_user_raises_ValidationError(self):
        with self.assertRaises(ValidationError) as context:
            User.update_user("pqr", {"email": "dot@com", "token": "357"})
        expected = context.exception.error_response_body()
        self.assertEqual(expected, {"error": "Missing: isAdmin"})
