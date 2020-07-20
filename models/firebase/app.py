import firebase_admin as fb  # type: ignore
import models.firebase.config as config_file


def authenticate(env):
    config = getattr(config_file, env)
    proj_id = config.PROJECT_ID
    cred_file = config.CREDENTIALS_FILE
    cred = fb.credentials.Certificate(f'./models/firebase/{cred_file}')
    fb.initialize_app(cred, {
        'projectId': f'{proj_id}',
        'storageBucket': f'{proj_id}.appspot.com'
    })
