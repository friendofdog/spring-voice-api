import functools
import logging


class HttpError(Exception):

    def __init__(self, error, message, code):
        self.error = error
        self.message = message
        self.code = code

    def error_response_body(self):
        return {
            "error": self.error,
            "message": self.message
        }

    def error_response_body_and_code(self):
        return self.error_response_body(), self.code


class CollectionNotFound(HttpError):

    def __init__(self, collection):
        self.error = "not_found"
        self.message = f'Collection {collection} not found'
        self.code = 404


class EntryAlreadyExists(HttpError):

    def __init__(self, entry_id, collection):
        self.error = "already_exists"
        self.message = f"{entry_id} already exists in {collection}"
        self.code = 409


class EntryNotFound(HttpError):

    def __init__(self, entry_id, collection):
        self.error = "not_found"
        self.message = f"{entry_id} was not found in {collection}"
        self.code = 404


class ServerError(Exception):

    def __init__(self, message, code):
        self.message = message
        self.code = code

    def error_response_body(self):
        return {'error': self.message, 'code': self.code}, self.code


class ValidationError(HttpError):

    def __init__(self, invalid, err_type):
        self.error = "validation_failure"
        self.message = self.create_validation_error_message(invalid, err_type)
        self.code = 400

    def create_validation_error_message(self, invalid, err_type):
        if err_type == "not_allowed":
            return f"Not allowed: {', '.join(invalid)}"
        if err_type == "missing":
            return f"Missing: {', '.join(invalid)}"
        if err_type == "type":
            message = [f"{e[0]} is {e[1]}, should be {e[2]}." for e in invalid]
            return f"Bad types: {', '.join(message)}"


class AuthorizationError(Exception):

    def __init__(self, message):
        self.message = message

    def error_response_body(self):
        return {'error': self.message}

    def error_response_body_and_code(self):
        return self.error_response_body(), 400


class AuthProviderResponseError(Exception):

    def __init__(self, message):
        self.message = message

    def error_response_body(self):
        return {'error': self.message}

    def error_response_body_and_code(self):
        return self.error_response_body(), 400


class MissingProjectId(Exception):

    def __init__(self, message):
        self.message = message

    def error_response_body(self):
        return {'error': self.message}

    def error_response_body_and_code(self):
        return self.error_response_body(), 400


class InvalidJSONURI(Exception):

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
    class HttpErrorAAA(Exception):

        def error_response_body(self):
            return {
                "error": error,
                "message": message
            }

        def error_response_body_and_code(self):
            return self.error_response_body(), code

    return HttpErrorAAA


MissingAuthorization = http_error(
    "unauthorized", "Request requires Authorization header", 401)


InvalidAuthHeaderValue = http_error(
    "bad_request", "Requires bearer token", 400)


InvalidAuthorization = http_error(
    "forbidden", "You are not authorized to perform this action", 403)
