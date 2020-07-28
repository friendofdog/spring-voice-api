import firebase_admin as auth  # type: ignore
import os


def authenticate():
    proj_id = os.getenv('PROJECT_ID')
    cred_file = os.getenv('CREDENTIALS_FILE')
    app = auth.credentials.Certificate(f'{cred_file}')
    auth.initialize_app(app, {
        'projectId': f'{proj_id}',
        'storageBucket': f'{proj_id}.appspot.com'
    })
