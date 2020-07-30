from firebase_admin import firestore  # type: ignore
from google.api_core import exceptions as google_exceptions  # type: ignore


def get_collection(collection):
    client = firestore.client()
    response = client.collection(f'{collection}').stream()
    collection_obj = {}
    for r in response:
        collection_obj[r.id] = r.to_dict()
    return collection_obj


def add_entry(collection, data, entry_id=None):
    client = firestore.client()
    try:
        __, response = client.collection(collection).add(data, entry_id)
        added = response.get().to_dict()
        status = '201 CREATED'
    except google_exceptions.AlreadyExists as e:
        added = str(e)
        status = '409 Conflict'
    return added, status


def update_entry(collection, data, entry_id):
    client = firestore.client()
    try:
        client.collection(collection).document(entry_id).update(data)
        updated = f'{entry_id} updated'
        status = '200 OK'
    except google_exceptions.NotFound as e:
        updated = str(e)
        status = '404 NOT FOUND'
    return updated, status
