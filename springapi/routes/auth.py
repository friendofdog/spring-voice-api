from springapi.helpers import make_route, VERSION


@make_route(f"/api/{VERSION}/auth", methods=['POST'])
def healthcheck(config, data):
    pass
