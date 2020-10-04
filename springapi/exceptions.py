import functools
import logging


class CollectionNotFound(Exception):

    def __init__(self, collection):
        self.message = f'Collection {collection} not found'

    def error_response_body(self):
        return {'error': self.message}

    def error_response_body_and_code(self):
        return self.error_response_body(), 404


class EntryAlreadyExists(Exception):

    def __init__(self, entry_id, collection):
        self.message = f'{entry_id} already exists in {collection}'

    def error_response_body(self):
        return {'error': self.message}

    def error_response_body_and_code(self):
        return self.error_response_body(), 409


class EntryNotFound(Exception):

    def __init__(self, entry_id, collection):
        self.message = f'{entry_id} was not found in {collection}'

    def error_response_body(self):
        return {'error': self.message}

    def error_response_body_and_code(self):
        return self.error_response_body(), 404


class ServerError(Exception):

    def __init__(self, message, code):
        self.message = message
        self.code = code

    def error_response_body(self):
        return {'error': self.message, 'code': self.code}, self.code


class ValidationError(Exception):

    def __init__(self, message):
        self.message = message

    def error_response_body(self):
        return {'error': self.message}

    def error_response_body_and_code(self):
        return self.error_response_body(), 400


def pretty_errors(fn):
    """
    Applies exceptions to the passed-in function, ensuring that if it fails
    when called an appropriate exception will be given.

    :param fn: func <springapi.routes.route.fn>
    :return: func <wrapper_fn>
    """

    @functools.wraps(fn)
    def wrapped_fn(*args, **kwargs):
        """
        :param args: dict, configuration
        :param kwargs: str, id of existing entry
        :return: dict or exception, response to a call to a route
        """

        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logging.exception("Error running route")
            if hasattr(e, "error_response_body_and_code"):
                return e.error_response_body_and_code()
            else:
                return {"error": "Unexpected server error"}, 500
    return wrapped_fn


def http_error(error, message, code):
    class HttpError(Exception):

        def error_response_body(self):
            return {
                "error": error,
                "message": message
            }

        def error_response_body_and_code(self):
            return self.error_response_body(), code

    return HttpError


MissingAuthorization = http_error(
    "unauthorized", "Request requires Authorization header", 401)


InvalidAuthHeaderValue = http_error(
    "bad_request", "Requires bearer token", 400)


InvalidAuthorization = http_error(
    "forbidden", "You are not authorized to perform this action", 403)
