from firebase_admin import firestore  # type: ignore


def get_collection(collection):
    db = firestore.client()
    collection_ref = db.collection(f'{collection}')
    submissions = collection_ref.stream()
    return submissions


def add_entry(data):
    pass


def update_entry(data):
    pass
