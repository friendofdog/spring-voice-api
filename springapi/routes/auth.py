from springapi.helpers import make_route, VERSION
from flask import request


@make_route(f"/api/{VERSION}/auth", methods=['GET', 'POST'])
def auth(config):
    return request.data
