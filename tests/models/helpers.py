import contextlib
import unittest
from unittest import mock

from springapi.exceptions import (
    EntryNotFound, CollectionNotFound, ValidationError, EntryAlreadyExists)
from springapi.models.helpers import create_uid
from tests.helpers import MockUid


def _create_validation_err_message(message, err_type):
    msg_prefixes = {
        "not_allowed": "Not allowed: ",
        "missing": "Missing: ",
        "type": "Bad types: "
    }
    return {
        "error": "validation_failure",
        "message": f"{msg_prefixes[err_type]}{message}"
    }


def _create_collection_not_found_err_message(collection):
    return {
        "error": "not_found",
        "message": f"Collection {collection} not found"
    }


def _create_entry_not_found_err_message(entry_id, collection):
    return {
        "error": "not_found",
        "message": f'{entry_id} was not found in {collection}'
    }


def _create_entry_already_exists_err_message(uid, collection):
    return {
        "error": "already_exists",
        "message": f"{uid} already exists in {collection}"
    }


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


class ModelResponseAssertions(ResponseAssertions):

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
        err = _create_collection_not_found_err_message(collection)

        with self._assert_expected_exception_and_error(
                exception, err):
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
        err = _create_validation_err_message(message, err_type)

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
        err = _create_entry_already_exists_err_message(uid, collection)

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
        err = _create_entry_not_found_err_message(entry_id, collection)

        with self._assert_expected_exception_and_error(exception, err):
            method(entry_id)
        mock_get.assert_called_with(collection, entry_id)

    @mock.patch('springapi.models.firebase.client.update_entry')
    def assert_update_single_entry_returns_success(
            self, collection, method, entry_id, data, mock_update):
        expected = mock_update.return_value = {"success": "yes"}
        self.assertEqual(
            expected, method(entry_id, data))
        mock_update.assert_called_with(collection, data, entry_id)

    @mock.patch('springapi.models.firebase.client.update_entry')
    def assert_update_single_entry_raises_EntryNotFound(
            self, collection, method, entry_id, data, mock_update):
        exception = EntryNotFound
        mock_update.side_effect = exception(entry_id, collection)
        err = _create_entry_not_found_err_message(entry_id, collection)

        with self._assert_expected_exception_and_error(exception, err):
            method(entry_id, data)
        mock_update.assert_called_with(collection, data, entry_id)

    @mock.patch('springapi.models.firebase.client.update_entry')
    def assert_update_single_entry_raises_ValidationError(
            self, method, data, message, err_type, mock_update):
        exception = ValidationError
        err = _create_validation_err_message(message, err_type)

        with self._assert_expected_exception_and_error(exception, err):
            method("1", data)
        self.assertFalse(mock_update.called)


class ClientResponseAssertions(ResponseAssertions):

    def assert_get_collection_returns_all_entries(
            self, collection, method, expected, field=None):
        entries = method(collection, field)

        self.assertDictEqual(entries, expected)

    def assert_get_collection_returns_filtered_entries(
            self, collection, method, valid, field, value):

        response = method(collection, field, value)
        self.assertTrue(response)
        self.assertListEqual(list(response.values()), valid)

    def assert_get_collection_raises_CollectionNotFound(
            self, collection, method):
        exception = CollectionNotFound
        err = _create_collection_not_found_err_message(collection)

        with self._assert_expected_exception_and_error(
                exception, err):
            method(collection)

    def assert_add_entry_raises_ValidationError(
            self, collection, method, data, message, err_type):
        exception = ValidationError
        err = _create_validation_err_message(message, err_type)

        with self._assert_expected_exception_and_error(exception, err):
            method(collection, data)
