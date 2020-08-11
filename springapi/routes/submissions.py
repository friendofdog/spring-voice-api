from springapi.helpers import route, VERSION
from springapi.models.exceptions import ValidationError, ServerError
from springapi.models.submission import Submission
from flask import request


@route(f"/api/{VERSION}/submissions", methods=['GET'])
def db_get_submissions():
    submission = Submission()
    submissions = submission.get_submissions()
    response = {"submissions": submissions}
    return response


@route(f"/api/{VERSION}/submissions/<entry_id>", methods=['GET'])
def db_get_submission(entry_id):
    submission = Submission()
    response, status = submission.get_submission(entry_id)
    data = {entry_id: response}
    return data, status


@route(f"/api/{VERSION}/submissions", methods=['POST'])
def db_create_submission():
    # request_data = request.data.decode('utf-8')
    request_data = request.args.to_dict()
    submission = Submission()
    try:
        response, status = submission.create_submission(request_data)
    except ValidationError as e:
        response, status = e.error_response_body(), 400
    except ServerError as e:
        response, status = e.error_response_body(), 500
    return response, status


@route(f"/api/{VERSION}/submissions/<entry_id>", methods=['PUT'])
def db_update_submission(entry_id):
    # request_data = request.data.decode('utf-8')
    request_data = request.args.to_dict()
    submission = Submission()
    response, status = submission.update_submission(request_data, entry_id)
    return response, status
