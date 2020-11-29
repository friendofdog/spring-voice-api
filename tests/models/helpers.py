import contextlib
import unittest
from unittest import mock

from springapi.exceptions import (
    EntryNotFound, CollectionNotFound, ValidationError, EntryAlreadyExists)
from springapi.models.helpers import create_uid
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

    @mock.patch('springapi.models.firebase.client.get_collection')
    def assert_get_collection_returns_all_valid_entries(
            self, collection, method, valid, invalid, mock_get):
        mock_get.return_value = {**valid, **invalid}
        response = method()
        entries = [r.to_json() for r in response]
        valid_entries = [valid[k] for k in valid]

        self.assertListEqual(entries, valid_entries)
        mock_get.assert_called_with(collection)

    @mock.patch('springapi.models.firebase.client.get_collection')
    def assert_get_collection_raises_CollectionNotFound(
            self, collection, method, mock_get):
        exception = CollectionNotFound
        mock_get.side_effect = exception(collection)

        with self._assert_expected_exception_and_error(
                exception, {
                    "error": "not_found",
                    "message": f"Collection {collection} not found"
                }):
            method()
        mock_get.assert_called_with(collection)

    @mock.patch('springapi.models.firebase.client.add_entry')
    @mock.patch('uuid.uuid4', MockUid.create_mock_uid)
    def assert_create_entry_returns_success(
            self, collection, cls, method, data, mock_add):
        entry_id = create_uid()
        mock_add.return_value = {entry_id: data}
        result = method(data)
        expected = cls.from_json(data)

        self.assertEqual(expected, result)
        mock_add.assert_called_with(collection, data)

    @mock.patch('springapi.models.firebase.client.add_entry')
    def assert_create_entry_raises_ValidationError(
            self, method, data, message, err_type, mock_add):
        exception = ValidationError
        msg_prefixes = {
            "not_allowed": "Not allowed: ",
            "missing": "Missing: ",
            "type": "Bad types: "
        }
        err = {
            "error": "validation_failure",
            "message": f"{msg_prefixes[err_type]}{message}"
        }

        with self._assert_expected_exception_and_error(exception, err):
            method(data)
        self.assertFalse(mock_add.called)

    @mock.patch('springapi.models.firebase.client.add_entry')
    @mock.patch('uuid.uuid4', MockUid.create_mock_uid)
    def assert_create_entry_raises_EntryAlreadyExists(
            self, collection, method, data, mock_add):
        exception = EntryAlreadyExists
        entry_id = create_uid()
        mock_add.side_effect = exception(entry_id, collection)
        uid = MockUid.get_mock_uid_base32()
        err = {
            "error": "already_exists",
            "message": f"{uid} already exists in {collection}"
        }

        with self._assert_expected_exception_and_error(exception, err):
            method(data)
        mock_add.assert_called_with(collection, data)

    @mock.patch('springapi.models.firebase.client.get_entry')
    def assert_get_single_entry_returns_entry(
            self, collection, cls, method, entry_id, expected, mock_get):
        mock_get.return_value = expected
        response = method(entry_id)
        response_json = cls.to_json(response)
        self.assertEqual(response_json, expected)
        mock_get.assert_called_with(collection, entry_id)

    @mock.patch('springapi.models.firebase.client.get_entry')
    def assert_get_single_entry_raises_EntryNotFound(
            self, collection, method, entry_id, mock_get):
        exception = EntryNotFound
        mock_get.side_effect = exception(entry_id, collection)
        err = {
            "error": "not_found",
            "message": f'{entry_id} was not found in {collection}'
        }

        with self._assert_expected_exception_and_error(exception, err):
            method(entry_id)
        mock_get.assert_called_with(collection, entry_id)

    @mock.patch('springapi.models.firebase.client.update_entry')
    def assert_update_single_entry_raises_EntryNotFound(
            self, collection, method, entry_id, data, mock_update):
        exception = EntryNotFound
        mock_update.side_effect = exception(entry_id, collection)
        err = {
            "error": "not_found",
            "message": f"{entry_id} was not found in {collection}"
        }

        with self._assert_expected_exception_and_error(exception, err):
            method(entry_id, data)
        mock_update.assert_called_with(collection, data, entry_id)

    @mock.patch('springapi.models.firebase.client.update_entry')
    def assert_update_single_entry_raises_ValidationError(
            self, method, data, message, err_type, mock_update):
        exception = ValidationError
        msg_prefixes = {
            "not_allowed": "Not allowed: ",
            "missing": "Missing: ",
            "type": "Bad types: "
        }
        err = {
            "error": "validation_failure",
            "message": f"{msg_prefixes[err_type]}{message}"
        }

        with self._assert_expected_exception_and_error(exception, err):
            method("1", data)
        self.assertFalse(mock_update.called)

    @mock.patch('springapi.models.firebase.client.update_entry')
    def assert_update_single_entry_returns_success(
            self, collection, method, entry_id, data, mock_update):
        expected = mock_update.return_value = {"success": "yes"}
        self.assertEqual(
            expected, method(entry_id, data))
        mock_update.assert_called_with(collection, data, entry_id)
