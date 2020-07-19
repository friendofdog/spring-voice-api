import firebase_admin as fb
import models.firebase.config as config_file


def authenticate():
    proj_id = config_file.ProductionConfig.PROJECT_ID
    cred = config_file.ProductionConfig.CREDENTIALS_FILE
    cred = fb.credentials.Certificate(f'./models/firebase/{cred}')
    fb.initialize_app(cred, {
        'projectId': f'{proj_id}',
        'storageBucket': f'{proj_id}.appspot.com'
    })
