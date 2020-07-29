from firebase_admin import firestore  # type: ignore


def get_collection(collection):
    db = firestore.client()
    collection_ref = db.collection(f'{collection}')
    collection_obj = collection_ref.stream()
    submissions = {}
    for e in collection_obj:
        submissions[e.id] = e.to_dict()
    return submissions


def add_entry(data):
    pass


def update_entry(data):
    pass
