from springapi.helpers import route, VERSION


@route(f"/api/{VERSION}/healthcheck", methods=['GET'])
def healthcheck():
    return {"success": True}, 200
