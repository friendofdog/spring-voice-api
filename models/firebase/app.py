import firebase_admin as fb
import models.firebase.config as config_file


def authenticate():
    proj_id = config_file.DevelopmentConfig.PROJECT_ID
    cred = config_file.DevelopmentConfig.CREDENTIALS_FILE
    cred = fb.credentials.Certificate(f'./models/firebase/{cred}')
    fb.initialize_app(cred, {
        'projectId': f'{proj_id}',
        'storageBucket': f'{proj_id}.appspot.com'
    })
