from springapi.config_helpers import decode_json_uri
from springapi.models.authorization import (
    get_auth_code_uri, exchange_oauth_token)
from springapi.exceptions import AuthorizationError
from springapi.helpers import make_route, VERSION, AUTH
from flask import redirect, request


@make_route(f"/api/{VERSION}/auth", methods=['GET'])
def request_auth_code(config):
    _, credentials = decode_json_uri(config[AUTH])
    redirect_host = request.host_url
    try:
        response = get_auth_code_uri(redirect_host, credentials)
    except AuthorizationError as e:
        return {"error": f"Could not retrieve authorization code: {e}"}, 400
    return redirect(response), 302


@make_route(f"/api/{VERSION}/auth-callback", methods=['GET'])
def request_exchange_token(config):
    _, credentials = decode_json_uri(config[AUTH])
    code = request.args.get("code")
    code_json = {"code": code}
    redirect_host = request.host_url
    try:
        response = exchange_oauth_token(code_json, credentials, redirect_host)
    except AuthorizationError as e:
        return {"error": f"Something went wrong with token exchange: {e}"}, 400
    return response
