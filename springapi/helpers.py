from springapi.models.exceptions import pretty_errors


VERSION = "v1"


def route(*route_args, **route_kwargs):
    def wrapper(fn):
        fn._route_args = route_args
        fn._route_kwargs = route_kwargs
        return pretty_errors(fn)
    return wrapper


def register(app, route):
    app.route(*route._route_args, **route._route_kwargs)(route)
