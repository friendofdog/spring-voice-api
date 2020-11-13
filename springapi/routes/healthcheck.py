from springapi.config_helpers import VERSION
from springapi.helpers import make_route


@make_route(f"/api/{VERSION}/healthcheck", methods=['GET'])
def healthcheck(config):
    return {"success": True}, 200
