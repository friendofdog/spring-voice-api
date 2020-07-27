import firebase_admin as auth  # type: ignore
from dotenv import load_dotenv
import os


def authenticate():
    load_dotenv()
    proj_id = os.getenv('PROJECT_ID')
    cred_file = os.getenv('CREDENTIALS_FILE')
    app = auth.credentials.Certificate(f'./models/firebase/{cred_file}')
    auth.initialize_app(app, {
        'projectId': f'{proj_id}',
        'storageBucket': f'{proj_id}.appspot.com'
    })
