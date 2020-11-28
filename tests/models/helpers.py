import contextlib
import unittest
from unittest import mock

from springapi.exceptions import (
    EntryNotFound, CollectionNotFound, ValidationError, EntryAlreadyExists)
from springapi.models.helpers import create_uid
from springapi.models.submission import (
    Submission, COLLECTION as COL_SUB)
from springapi.models.token import Token, COLLECTION as COL_TOK
from tests.helpers import MockUid


class ResponseAssertions(unittest.TestCase):

    @contextlib.contextmanager
    def _assert_expected_exception_and_error(
            self, expected_exception, expected_err=None):
        with self.assertRaises(expected_exception) as context:
            yield

        if expected_err is not None:
            self.assertEqual(
                context.exception.error_response_body(),
                expected_err)

    @contextlib.contextmanager
    def _assert_expected_exception_and_error_temp(
            self, expected_exception, expected_err=None):
        with self.assertRaises(expected_exception) as context:
            yield

        if expected_err is not None:
            self.assertEqual(
                context.exception.error_response_body(),
                expected_err)

    @mock.patch('springapi.models.firebase.client.get_collection')
    def _assert_get_collection_returns_all_valid_entries(
            self, collection, method, valid, invalid, mock_get):
        mock_get.return_value = {**valid, **invalid}
        response = method()
        entries = [r.to_json() for r in response]
        valid_entries = [valid[k] for k in valid]

        self.assertListEqual(entries, valid_entries)
        mock_get.assert_called_with(collection)

    @mock.patch('springapi.models.firebase.client.get_collection')
    def _assert_get_collection_raises_CollectionNotFound(
            self, collection, method, mock_get):
        exception = CollectionNotFound
        mock_get.side_effect = exception(collection)

        with self._assert_expected_exception_and_error(
                exception, {"error": f"Collection {collection} not found"}):
            method()
        mock_get.assert_called_with(collection)

    @mock.patch('springapi.models.firebase.client.add_entry')
    @mock.patch('uuid.uuid4', MockUid.create_mock_uid)
    def _assert_create_entry_returns_success(
            self, collection, cls, method, data, mock_add):
        entry_id = create_uid()
        mock_add.return_value = {entry_id: data}
        result = method(data)
        expected = cls.from_json(data)

        self.assertEqual(expected, result)
        mock_add.assert_called_with(collection, data)

    @mock.patch('springapi.models.firebase.client.add_entry')
    def _assert_create_entry_raises_ValidationError(
            self, method, data, err, mock_add):
        exception = ValidationError

        with self._assert_expected_exception_and_error_temp(exception, err):
            method(data)
        self.assertFalse(mock_add.called)

    @mock.patch('springapi.models.firebase.client.add_entry')
    @mock.patch('uuid.uuid4', MockUid.create_mock_uid)
    def _assert_create_entry_raises_EntryAlreadyExists(
            self, collection, method, data, err, mock_add):
        exception = EntryAlreadyExists
        entry_id = create_uid()
        mock_add.side_effect = exception(entry_id, collection)

        with self._assert_expected_exception_and_error_temp(exception, err):
            method(data)
        mock_add.assert_called_with(collection, data)

    @mock.patch('springapi.models.firebase.client.get_entry')
    def _assert_get_single_entry_returns_entry(
            self, collection, cls, method, entry_id, expected, mock_get):
        mock_get.return_value = expected
        response = method(entry_id)
        response_json = cls.to_json(response)
        self.assertEqual(response_json, expected)
        mock_get.assert_called_with(collection, entry_id)

    @mock.patch('springapi.models.firebase.client.get_entry')
    def _assert_get_single_entry_raises_EntryNotFound(
            self, collection, method, entry_id, err, mock_get):
        exception = EntryNotFound
        mock_get.side_effect = exception(entry_id, collection)

        with self._assert_expected_exception_and_error_temp(exception, err):
            method(entry_id)
        mock_get.assert_called_with(collection, entry_id)

    @mock.patch('springapi.models.firebase.client.update_entry')
    def _assert_update_single_entry_raises_EntryNotFound(
            self, collection, method, entry_id, data, err, mock_update):
        exception = EntryNotFound
        mock_update.side_effect = exception(entry_id, collection)
        with self._assert_expected_exception_and_error_temp(exception, err):
            method(entry_id, data)
        mock_update.assert_called_with(collection, data, entry_id)

    @mock.patch('springapi.models.firebase.client.update_entry')
    def _assert_update_single_entry_raises_ValidationError(
            self, method, entry_id, data, err, mock_update):
        exception = ValidationError

        with self._assert_expected_exception_and_error_temp(exception, err):
            method(entry_id, data)
        self.assertFalse(mock_update.called)

    @mock.patch('springapi.models.firebase.client.update_entry')
    def _assert_update_single_entry_returns_success(
            self, collection, method, entry_id, data, mock_update):
        expected = mock_update.return_value = {"success": "yes"}
        self.assertEqual(
            expected, method(entry_id, data))
        mock_update.assert_called_with(collection, data, entry_id)


class TokenResponseAssertions(ResponseAssertions):

    def assert_get_tokens_returns_all_valid_tokens(self, valid, invalid):
        self._assert_get_collection_returns_all_valid_entries(
            COL_TOK, Token.get_tokens, valid, invalid)

    def assert_get_tokens_raises_CollectionNotFound(self):
        self._assert_get_collection_raises_CollectionNotFound(
            COL_TOK, Token.get_tokens)

    def assert_create_token_returns_success(self, data):
        self._assert_create_entry_returns_success(
            COL_TOK, Token, Token.create_token, data)

    def assert_create_token_raises_ValidationError(self, data, err):
        self._assert_create_entry_raises_ValidationError(
            Token.create_token, data, err)

    def assert_create_token_raises_EntryAlreadyExists(self, data, err):
        self._assert_create_entry_raises_EntryAlreadyExists(
            COL_TOK, Token.create_token, data, err)


class SubmissionResponseAssertions(ResponseAssertions):

    def assert_get_submissions_returns_all_valid_submissions(
            self, valid, invalid):
        self._assert_get_collection_returns_all_valid_entries(
            COL_SUB, Submission.get_submissions, valid, invalid)

    def assert_get_submissions_raises_CollectionNotFound(self):
        self._assert_get_collection_raises_CollectionNotFound(
            COL_SUB, Submission.get_submissions)

    def assert_get_single_submission_raises_EntryNotFound(self, entry_id, err):
        self._assert_get_single_entry_raises_EntryNotFound(
            COL_SUB, Submission.get_submission, entry_id, err)

    def assert_get_single_submission_returns_single(self, entry_id, expected):
        self._assert_get_single_entry_returns_entry(
            COL_SUB, Submission, Submission.get_submission, entry_id, expected)

    def assert_create_submission_returns_success(self, data):
        self._assert_create_entry_returns_success(
            COL_SUB, Submission, Submission.create_submission, data)

    def assert_create_submission_raises_ValidationError(self, data, err):
        self._assert_create_entry_raises_ValidationError(
            Submission.create_submission, data, err)

    def assert_create_submission_raises_AlreadyExists(self, data, err):
        self._assert_create_entry_raises_EntryAlreadyExists(
            COL_SUB, Submission.create_submission, data, err)

    def assert_update_submission_returns_success(self, entry_id, data):
        self._assert_update_single_entry_returns_success(
            COL_SUB, Submission.update_submission, entry_id, data)

    def assert_update_submission_raises_EntryNotFound(
            self, entry_id, data, err):
        self._assert_update_single_entry_raises_EntryNotFound(
            COL_SUB, Submission.update_submission, entry_id, data, err)

    def assert_update_submission_raises_ValidationError(
            self, entry_id, data, err):
        self._assert_update_single_entry_raises_ValidationError(
            Submission.update_submission, entry_id, data, err)
