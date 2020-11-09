import unittest
from springapi.models.email import Email
from unittest import mock


@mock.patch('springapi.models.firebase.client.get_email_addresses')
class TestUserGetAuthorizedEmails(unittest.TestCase):

    def test_get_authorized_emails_returns_email_list(self, mock_addr):
        expected = mock_addr.return_value = ["foo@bar"]
        email_list = Email.get_authorized_emails()
        self.assertEqual(email_list, expected)
