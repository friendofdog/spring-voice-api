from springapi.helpers import route, VERSION
from springapi.models.firebase.client \
    import get_collection, add_entry, update_entry
from flask import request, jsonify


@route(f"/api/{VERSION}/submissions", methods=['GET'])
def get_submissions():
    submissions = get_collection('submissions')
    response = {"submissions": submissions}
    return response


@route(f"/api/{VERSION}/submissions", methods=['POST'])
def create_submission():
    request_data = request.data.decode('utf-8')
    response, status = add_entry('submissions', request_data)
    return response, status


@route(f"/api/{VERSION}/submissions", methods=['PUT'])
def update_submission():
    request_data = request.data.decode('utf-8')
    response, status = update_entry(request_data)
    return jsonify(response), status
