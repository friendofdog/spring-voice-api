import urllib.parse
from firebase_admin import storage  # type: ignore


def get_image(blob_name, img_dir):
    bucket = storage.bucket()
    base_url = 'https://firebasestorage.googleapis.com/v0/b/'
    full_name = f"{f'{img_dir}%2F' if img_dir else ''}{blob_name}"
    blob = bucket.blob(urllib.parse.unquote(full_name))
    if blob.exists():
        image = {
            'public_url':
                f"{base_url}{blob.bucket.name}/o/{full_name}?alt=media",
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
