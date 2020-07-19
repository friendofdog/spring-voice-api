from firebase_admin import storage  # type: ignore


def get_images():
    bucket = storage.bucket()
    blobs = bucket.list_blobs()
    return blobs


def get_image(blob_name):
    bucket = storage.bucket()
    blob = bucket.blob(f'submissions/{blob_name}')
    if blob.exists():
        image = {
            'public_url':
                f'https://firebasestorage.googleapis.com/v0/b/{blob.bucket.name}/o/submissions%2F{blob.name}?alt=media',
            'name': blob.name,
            'meta': blob.metadata
        }
    else:
        image = {}
    return image


def upload_image(blob_name, source_file):
    bucket = storage.bucket()
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(source_file)
