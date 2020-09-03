from firebase_admin import firestore  # type: ignore
from google.api_core import exceptions as google_exceptions  # type: ignore
from springapi.models.exceptions import \
    CollectionNotFound, EntryAlreadyExists, EntryNotFound


def get_collection(collection):
    client = firestore.client()
    response = client.collection(f'{collection}')
    collection_obj = {}
    for r in response.stream():
        collection_obj[r.id] = r.to_dict()
    if collection_obj:
        return collection_obj
    else:
        raise CollectionNotFound(collection)


def get_entry(collection, entry_id):
    client = firestore.client()
    response = client.collection(collection).document(entry_id).get()
    entry = response.to_dict()
    if entry:
        return entry
    else:
        raise EntryNotFound(entry_id, collection)


def add_entry(collection, data, entry_id=None):
    client = firestore.client()
    try:
        __, response = client.collection(collection).add(data, entry_id)
        added = {response.get().id: response.get().to_dict()}
        return added
    except google_exceptions.AlreadyExists:
        raise EntryAlreadyExists(entry_id, collection)


def update_entry(collection, data, entry_id):
    client = firestore.client()
    try:
        client.collection(collection).document(entry_id).update(data)
        return f'{entry_id} updated'
    except google_exceptions.NotFound:
        raise EntryNotFound(entry_id, collection)
