from springapi.helpers import make_route, VERSION


@make_route(f"/api/{VERSION}/healthcheck", methods=['GET'])
def healthcheck(config):
    return {"success": True}, 200
