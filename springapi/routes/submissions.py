from springapi.helpers import route, VERSION
from springapi.models.submission import Submission
from flask import request


@route(f"/api/{VERSION}/submissions", methods=['GET'])
def get_all():
    submission = Submission()
    submissions = submission.get_submissions()
    return {"submissions": submissions}, 200


@route(f"/api/{VERSION}/submissions/<entry_id>", methods=['GET'])
def get_single(entry_id):
    submission = Submission()
    data = submission.get_submission(entry_id)
    return {entry_id: data}, 200


@route(f"/api/{VERSION}/submissions", methods=['POST'])
def create_single():
    request_data = request.args.to_dict()
    submission = Submission()
    return submission.create_submission(request_data), 201


@route(f"/api/{VERSION}/submissions/<entry_id>", methods=['PUT'])
def update_single(entry_id):
    data = request.args.to_dict()
    submission = Submission()
    return submission.update_submission(entry_id, data), 200
