import json
from springapi.models.authorization import get_auth_code, exchange_token
from springapi.exceptions import AuthorizationError
from springapi.helpers import make_route, VERSION
from flask import request


@make_route(f"/api/{VERSION}/auth", methods=['POST'])
def request_auth_code(config):
    try:
        request_data = json.loads(request.data)
        response = get_auth_code(request_data)
    except ValueError:
        return {"error": "Invalid JSON"}, 400
    except AuthorizationError as e:
        return {"error": f"Something went wrong with authorization: {e}"}, 400
    return response, 200


@make_route(f"/api/{VERSION}/auth-callback", methods=['GET'])
def request_exchange_token(config):
    try:
        code = request.args.get("code")
        code_json = {"code": code}
        response = exchange_token(code_json)
    except AuthorizationError as e:
        return {"error": f"Something went wrong with token exchange: {e}"}, 400
    return response
