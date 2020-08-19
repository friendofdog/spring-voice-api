import json
import tempfile

import firebase_admin as auth  # type: ignore
from springapi.config_helpers import decode_json_uri


def authenticate(uri):
    # Project ID -- should it come from query parameter?
    _, config = decode_json_uri(uri)
    with tempfile.NamedTemporaryFile(suffix=".json") as cred_file:
        cred_file.write(json.dumps(config).encode("utf8"))
        cred_file.seek(0)
        app = auth.credentials.Certificate(cred_file.name)
    auth.initialize_app(app, {
        'projectId': app.project_id,
        'storageBucket': f'{app.project_id}.appspot.com'
    })
