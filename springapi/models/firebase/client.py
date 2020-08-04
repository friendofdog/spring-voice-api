from firebase_admin import firestore  # type: ignore
from google.api_core import exceptions as google_exceptions  # type: ignore


def get_collection(collection):
    client = firestore.client()
    response = client.collection(f'{collection}').stream()
    collection_obj = {}
    for r in response:
        collection_obj[r.id] = r.to_dict()
    return collection_obj


def get_entry(collection, entry_id):
    client = firestore.client()
    response = client.collection(collection).document(entry_id).get()
    entry = response.to_dict()
    return entry


def add_entry(collection, data, entry_id=None):
    client = firestore.client()
    try:
        __, response = client.collection(collection).add(data, entry_id)
        added = {response.get().id: response.get().to_dict()}
        status = '201 CREATED'
    except google_exceptions.AlreadyExists:
        added = f'{entry_id} already exists'
        status = '409 Conflict'
    return added, status


def update_entry(collection, data, entry_id):
    client = firestore.client()
    try:
        client.collection(collection).document(entry_id).update(data)
        updated = f'{entry_id} updated'
        status = '200 OK'
    except google_exceptions.NotFound:
        updated = f'{entry_id} not found'
        status = '404 NOT FOUND'
    except google_exceptions.NotModified:
        updated = f'{entry_id} not modified'
        status = '304 NOT MODIFIED'
    return updated, status
