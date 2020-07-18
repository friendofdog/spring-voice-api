from firebase_admin import firestore


def get_collection(collection):
    db = firestore.client()
    collection_ref = db.collection(f'{collection}')
    submissions = collection_ref.stream()
    return submissions
