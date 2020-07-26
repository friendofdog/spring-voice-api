from springapi.helpers import route, VERSION
from models.firebase.db import get_collection, add_entry, update_entry
from flask import request, jsonify


@route(f"/api/{VERSION}/submissions", methods=['GET'])
def get_submissions():
    submissions = get_collection('submissions')
    response = {"submissions": submissions}
    return response


@route(f"/api/{VERSION}/submission", methods=['POST'])
def create_submission():
    request_data = request.data.decode('utf-8')
    response = add_entry(request_data)
    return jsonify(response)


@route(f"/api/{VERSION}/submission", methods=['PUT'])
def update_submission():
    request_data = request.data.decode('utf-8')
    response = update_entry(request_data)
    return jsonify(response)
