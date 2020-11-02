from springapi.config_helpers import decode_json_uri
from springapi.models.authorization import get_auth_code_uri, exchange_token
from springapi.exceptions import AuthorizationError
from springapi.helpers import make_route, VERSION, AUTH
from flask import redirect, request


@make_route(f"/api/{VERSION}/auth", methods=['GET'])
def request_auth_code(config):
    _, credentials = decode_json_uri(config[AUTH])
    try:
        redirect_host = f"{request.host_url}"
        response = get_auth_code_uri(redirect_host, credentials)
    except AuthorizationError as e:
        return {"error": f"Something went wrong with authorization: {e}"}, 400
    return redirect(response), 302


@make_route(f"/api/{VERSION}/auth-callback", methods=['POST'])
def request_exchange_token(config):
    try:
        code = request.args.get("code")
        code_json = {"code": code}
        response = exchange_token(code_json)
    except AuthorizationError as e:
        return {"error": f"Something went wrong with token exchange: {e}"}, 400
    return response
