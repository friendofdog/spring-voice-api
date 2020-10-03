from firebase_admin import firestore  # type: ignore
from google.api_core import exceptions as google_exceptions  # type: ignore
from springapi.exceptions import \
    CollectionNotFound, EntryAlreadyExists, EntryNotFound, ValidationError


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


def add_entry(collection, data):
    client = firestore.client()
    entry_id = data.pop('id', None)
    if entry_id is None:
        raise ValidationError('Entry ID missing')
    try:
        __, response = client.collection(collection).add(data, entry_id)
        added = {response.get().id: response.get().to_dict()}
        added[entry_id].update({"id": entry_id})
        return added
    except google_exceptions.AlreadyExists:
        raise EntryAlreadyExists(entry_id, collection)


def update_entry(collection, data, entry_id):
    client = firestore.client()
    data.pop('id', None)
    try:
        client.collection(collection).document(entry_id).update(data)
        return {'success': f'{entry_id} updated in {collection}'}
    except google_exceptions.NotFound:
        raise EntryNotFound(entry_id, collection)
