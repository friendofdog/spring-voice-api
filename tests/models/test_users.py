import unittest
from springapi.models.users import get_users
from unittest import mock


@mock.patch('springapi.models.users.get_firebase_users')
@mock.patch('springapi.models.users.authenticate_firebase')
@mock.patch('springapi.models.users.admin.get_app')
class TestUsers(unittest.TestCase):

    def test_get_users_returns_list_after_authentication(
            self, mock_admin, mock_auth, mock_users):
        mock_admin.return_value = []
        mock_auth.return_value = True
        expected = mock_users.return_value = ["a", "b", "c"]
        users = get_users("firebase", "http://uri")
        self.assertEqual(users, expected)
        mock_auth.assert_called_with("http://uri")

    def test_get_users_does_not_authenticate_if_firebase_app_initialised(
            self, mock_admin, mock_auth, mock_users):
        mock_admin.return_value = ["a"]
        mock_auth.return_value = True
        mock_users.return_value = ["a", "b", "c"]
        get_users("firebase", "http://uri")
        assert not mock_auth.called

    def test_get_authorized_users_raises_ValueError_bad_scheme(
            self, mock_admin, mock_auth, mock_users):
        mock_admin.return_value = ["a"]
        mock_auth.return_value = True
        mock_users.return_value = ["a", "b", "c"]
        scheme = "badscheme"
        with self.assertRaises(ValueError) as context:
            get_users(scheme, "http://uri")
        self.assertEqual(str(context.exception),
                         f'Unknown user database protocol: {scheme}')
