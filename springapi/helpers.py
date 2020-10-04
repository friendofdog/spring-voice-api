import functools

from flask import request
from springapi.exceptions import pretty_errors, \
    MissingAuthorization, InvalidAuthHeaderValue, InvalidAuthorization


VERSION = "v1"


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


def requires_admin(original_route):
    @functools.wraps(original_route)
    def wrapper(config, *args, **kwargs):
        if "Authorization" not in request.headers:
            raise MissingAuthorization()
        auth_header_value = request.headers["Authorization"]
        if not auth_header_value.startswith("Bearer "):
            raise InvalidAuthHeaderValue()
        auth_token_value = auth_header_value.split("Bearer ", 1)[1]
        if auth_token_value != config["ADMIN_TOKEN"]:
            raise InvalidAuthorization()
        return original_route(config, *args, **kwargs)
    return wrapper
