from flask import jsonify
from springapi.helpers import route, VERSION
from models.firebase.db import get_collection


@route(f"/api/{VERSION}/submissions", methods=['GET'])
def get_submissions():
    sumbissions = []
    documents = get_collection('submissions')
    for doc in documents:
        submission = {f'{doc.id}': doc.to_dict()}
        sumbissions.append(submission)
    return jsonify(sumbissions), 200
