from firebase_admin import storage


def get_uploaded_images():
    bucket = storage.bucket()
    blobs = bucket.list_blobs()
    return blobs
