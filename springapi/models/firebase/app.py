import firebase_admin as auth  # type: ignore
import os


def authenticate():
    proj_id = os.getenv('PROJECT_ID')
    cred_file = os.getenv('CREDENTIALS_FILE')
    cred_path = f'springapi/models/firebase/{cred_file}'
    app = auth.credentials.Certificate(cred_path)
    auth.initialize_app(app, {
        'projectId': f'{proj_id}',
        'storageBucket': f'{proj_id}.appspot.com'
    })
