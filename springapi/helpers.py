import functools

from flask import request
from springapi.exceptions import pretty_errors, \
    MissingAuthorization, InvalidAuthHeaderValue, InvalidAuthorization


VERSION = "v1"


def route(*route_args, **route_kwargs):
    def wrapper(fn):
        fn.route_args = route_args
        fn.route_kwargs = route_kwargs
        return pretty_errors(fn)
    return wrapper


def register(app, reg_route):

    @functools.wraps(reg_route)
    def config_route(*args, **kwargs):
        return reg_route(app.config, *args, **kwargs)

    app.route(*reg_route.route_args, **reg_route.route_kwargs)(config_route)


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
