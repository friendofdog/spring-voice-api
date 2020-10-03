from springapi.helpers import route, VERSION


@route(f"/api/{VERSION}/healthcheck", methods=['GET'])
def healthcheck(config):
    return {"success": True}, 200
