from firebase_admin import firestore  # type: ignore


def get_collection(collection):
    db = firestore.client()
    collection_obj = db.collection(f'{collection}').stream()
    submissions = {}
    for e in collection_obj:
        submissions[e.id] = e.to_dict()
    return submissions


def add_entry(collection, data):
    db = firestore.client()
    try:
        __, response = db.collection(collection).add(data)
        entry = response.get().to_dict()
        status = '201 CREATED'
    except Exception as e:
        entry = str(e)
        status = '500 INTERNAL SERVER ERROR'
    return entry, status


def update_entry(data):
    pass
