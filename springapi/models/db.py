import springapi.models.firebase.client as client


def get_submissions():
    return client.get_collection('submissions')
