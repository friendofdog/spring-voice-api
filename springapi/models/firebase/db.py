from firebase_admin import firestore  # type: ignore
from google.api_core import exceptions as google_exceptions


def get_collection(collection):
    db = firestore.client()
    collection_obj = db.collection(f'{collection}').stream()
    submissions = {}
    for e in collection_obj:
        submissions[e.id] = e.to_dict()
    return submissions


def add_entry(collection, data, entry_id=None):
    db = firestore.client()
    try:
        __, response = db.collection(collection).add(data, entry_id)
        added = response.get().to_dict()
        status = '201 CREATED'
    except google_exceptions.AlreadyExists as e:
        added = str(e)
        status = '409 Conflict'
    return added, status


def update_entry(collection, data, entry_id):
    db = firestore.client()
    try:
        db.collection(collection).document(entry_id).update(data)
        updated = f'{entry_id} updated'
        status = '200 OK'
    except google_exceptions.NotFound as e:
        updated = str(e)
        status = '404 NOT FOUND'
    return updated, status
