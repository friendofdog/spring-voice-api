from springapi.helpers import route, VERSION
from models.firebase.db import get_collection


@route(f"/api/{VERSION}/submissions", methods=['GET'])
def get_submissions():
    submissions = get_collection('submissions')
    response = {"submissions": submissions}
    return response
