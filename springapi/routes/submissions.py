from springapi.helpers import route, VERSION
from springapi.models.exceptions import *
from springapi.models.submission import Submission
from flask import request


@route(f"/api/{VERSION}/submissions", methods=['GET'])
def get_all():
    try:
        submission = Submission()
        submissions = submission.get_submissions()
        response, status = {"submissions": submissions}, 200
    except CollectionNotFound as err:
        response, status = err.error_response_body(), 404
    return response, status

@route(f"/api/{VERSION}/submissions/<entry_id>", methods=['GET'])
def get_single(entry_id):
    try:
        submission = Submission()
        data = submission.get_submission(entry_id)
        response, status = {entry_id: data}, 200
    except EntryNotFound as err:
        response, status = err.error_response_body(), 404
    return response, status


@route(f"/api/{VERSION}/submissions", methods=['POST'])
def create_single():
    try:
        # request_data = request.data.decode('utf-8')
        request_data = request.args.to_dict()
        submission = Submission()
        response, status = submission.create_submission(request_data), 201
    except ValidationError as e:
        response, status = e.error_response_body(), 400
    except EntryAlreadyExists as e:
        response, status = e.error_response_body(), 409
    except ServerError as e:
        response, status = e.error_response_body(), 500
    return response, status


@route(f"/api/{VERSION}/submissions/<entry_id>", methods=['PUT'])
def update_single(entry_id):
    try:
        # data = request.data.decode('utf-8')
        data = request.args.to_dict()
        print('r', data)
        submission = Submission()
        response, status = submission.update_submission(
            entry_id, data), 200
    except ValidationError as e:
        response, status = e.error_response_body(), 400
    except EntryNotFound as e:
        response, status = e.error_response_body(), 404
    except ServerError as e:
        response, status = e.error_response_body(), 500
    return response, status
