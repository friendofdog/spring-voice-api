from springapi.helpers import route, VERSION
from flask import jsonify


@route(f"/api/{VERSION}/healthcheck", methods=['GET'])
def healthcheck():
    try:
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An error occured: {e}"
