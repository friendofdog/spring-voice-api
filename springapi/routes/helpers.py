import functools
from flask import request

from springapi.exceptions import (
    pretty_errors, MissingAuthorization, InvalidAuthHeaderValue,
    InvalidAuthorization)
from springapi.models.token import Token


def make_route(*route_args, **route_kwargs):
    """
    Takes a route function and applies pretty_errors to it, ensuring that if
    the function fails when called it will throw an appropriate exception.

    :param route_args: str
    :param route_kwargs: list
    :return: func <springapi.routes.route.fn>
    """

    def config_pretty_errors(fn):
        """
        :param fn: func
        :return: func <pretty_errors>
        """
        fn.route_args = route_args
        fn.route_kwargs = route_kwargs
        return pretty_errors(fn)

    return config_pretty_errors


def register(app, fn):
    """
    Registers a route using Flask's route() method. Depends on make_route() to
    set attributes, so calling function nests this function after make_route().

    :param app: obj <springapi.app>, instance of Flask
    :param fn: func <springapi.routes.route.fn>
    :return: None
    """

    @functools.wraps(fn)
    def config_route(**kwargs):
        """
        :param kwargs: str, id of existing entry
        :return: dict or exception
        """

        return fn(app.config, **kwargs)

    app.route(*fn.route_args, **fn.route_kwargs)(config_route)


def get_valid_admin_tokens():
    tokens = [t.to_json()["token"] for t in Token.get_tokens()]
    return tokens


def requires_admin(original_route):
    """
    Checks config of route, returning the route if authorization passes and
    returning an exception if not.

    :param original_route: <springapi.routes.route.fn>
    :return: func <springapi.routes.route.fn>
    """
    @functools.wraps(original_route)
    def wrapper(config, *args, **kwargs):
        if "Authorization" not in request.headers:
            raise MissingAuthorization()
        auth_header_value = request.headers["Authorization"]
        if not auth_header_value.startswith("Bearer "):
            raise InvalidAuthHeaderValue()
        auth_token_value = auth_header_value.split("Bearer ", 1)[1]
        tokens = get_valid_admin_tokens()
        if auth_token_value not in tokens:
            raise InvalidAuthorization()
        return original_route(config, *args, **kwargs)
    return wrapper


def checks_authentication(original_route):
    def wrapper(config, *args, **kwargs):
        if "Authorization" in request.headers:
            auth_header_value = request.headers["Authorization"]
            if auth_header_value.startswith("Bearer "):
                auth_token_value = auth_header_value.split("Bearer ", 1)[1]
                tokens = get_valid_admin_tokens()
                if auth_token_value in tokens:
                    return {"status": "Valid token found in request header"}
        return original_route(config, *args, **kwargs)
    return wrapper
