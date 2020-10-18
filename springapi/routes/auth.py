from springapi.helpers import make_route, VERSION
from flask import request


@make_route(f"/api/{VERSION}/auth", methods=['GET'])
def auth(config):
    try:
        code = request.args.get("code")
        assert code
        code_json = {"code": code}
    except AssertionError:
        return {"error": "Authorization code not found"}, 400
    return code_json
