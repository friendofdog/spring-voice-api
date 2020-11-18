from springapi.config_helpers import VERSION, AUTH, CLIENT_ID
from springapi.exceptions import AuthorizationError
from springapi.helpers import make_route
from springapi.utils.authorization import get_auth_code_uri, create_api_token
from flask import redirect, request, Response


@make_route(f"/api/{VERSION}/auth", methods=['GET'])
def request_auth_code(config):
    client_id = config[CLIENT_ID]
    redirect_host = request.host_url
    redirect_url = get_auth_code_uri(redirect_host, client_id)
    return redirect(redirect_url), 302


@make_route(f"/api/{VERSION}/auth-callback", methods=['GET'])
def request_exchange_token(config):
    credentials = config[AUTH]
    code = request.args.get("code")
    code_json = {"code": code}
    redirect_host = request.host_url
    try:
        api_token = create_api_token(code_json, credentials, redirect_host)
    except AuthorizationError as e:
        return {"error": f"Something went wrong with token exchange: {e}"}, 400
    response = Response()
    response.headers["token"] = api_token
    return response, 200
