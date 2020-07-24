from flask import jsonify
from springapi.helpers import route, VERSION
from models.firebase.db import get_collection
from models.firebase.media import get_image


@route(f"/api/{VERSION}/submissions", methods=['GET'])
def get_submissions():
    return {"submissions": []}
    # documents = get_collection('submissions')
    # submissions = []
    # for doc in documents:
    #     submission = doc.to_dict()
    #     submission.update(get_image(doc.id, 'submissions'))
    #     submission.update(id=doc.id)
    #     submissions.append(submission)
    # return jsonify(submissions), 200
