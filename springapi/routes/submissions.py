from springapi.helpers import route, VERSION
from springapi.models.db import Submission, get_submissions, get_submission
from flask import request


@route(f"/api/{VERSION}/submissions", methods=['GET'])
def db_get_submissions():
    submissions = get_submissions()
    response = {"submissions": submissions}
    return response


@route(f"/api/{VERSION}/submissions/<entry_id>", methods=['GET'])
def db_get_submission(entry_id):
    submission, status = get_submission(entry_id)
    response = {entry_id: submission}
    return response, status


@route(f"/api/{VERSION}/submissions", methods=['POST'])
def db_create_submission():
    # request_data = request.data.decode('utf-8')
    request_data = request.args.to_dict()
    submission = Submission()
    response, status = submission.create_submission(request_data)
    return response, status


@route(f"/api/{VERSION}/submissions/<entry_id>", methods=['PUT'])
def db_update_submission(entry_id):
    # request_data = request.data.decode('utf-8')
    request_data = request.args.to_dict()
    submission = Submission()
    response, status = submission.update_submission(request_data, entry_id)
    return response, status
