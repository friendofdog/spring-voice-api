import json
from springapi.helpers import route, VERSION
from springapi.models.submission import Submission
from flask import request


@route(f"/api/{VERSION}/submissions", methods=['GET'])
def get_all():
    submissions = [s.to_json() for s in Submission.get_submissions()]
    return {"submissions": submissions}, 200


@route(f"/api/{VERSION}/submissions/<entry_id>", methods=['GET'])
def get_single(entry_id):
    submission = Submission.get_submission(entry_id)
    return submission.to_json(), 200


@route(f"/api/{VERSION}/submissions", methods=['POST'])
def create_single():
    try:
        request_data = json.loads(request.data)
    except ValueError:
        return {"error": "Invalid JSON"}, 400
    return Submission.create_submission(request_data).to_json(), 201


@route(f"/api/{VERSION}/submissions/<entry_id>", methods=['PUT'])
def update_single(entry_id):
    try:
        request_data = json.loads(request.data)
    except ValueError:
        return {"error": "Invalid JSON"}, 400
    return Submission.update_submission(entry_id, request_data).to_json(), 200
