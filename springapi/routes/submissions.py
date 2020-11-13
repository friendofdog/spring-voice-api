import json
from springapi.config_helpers import VERSION
from springapi.helpers import make_route, requires_admin
from springapi.models.submission import Submission
from flask import request


@make_route(f"/api/{VERSION}/submissions", methods=['GET'])
@requires_admin
def get_all(config):
    submissions = [s.to_json() for s in Submission.get_submissions()]
    return {"submissions": submissions}, 200


@make_route(f"/api/{VERSION}/submissions/<entry_id>", methods=['GET'])
@requires_admin
def get_single(config, entry_id):
    try:
        submission = Submission.get_submission(entry_id)
    except ValueError as err:
        return {"error": f"{entry_id} contains data which has failed "
                         f"validation - {err}"}, 400
    return submission.to_json(), 200


@make_route(f"/api/{VERSION}/submissions", methods=['POST'])
def create_single(config):
    try:
        request_data = json.loads(request.data)
    except ValueError:
        return {"error": "Invalid JSON"}, 400
    return Submission.create_submission(request_data).to_json(), 201


@make_route(f"/api/{VERSION}/submissions/<entry_id>", methods=['PUT'])
@requires_admin
def update_single(config, entry_id):
    try:
        request_data = json.loads(request.data)
    except ValueError:
        return {"error": "Invalid JSON"}, 400
    return Submission.update_submission(entry_id, request_data), 200
