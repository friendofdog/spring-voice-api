import firebase_admin as admin  # type: ignore
from springapi.models.firebase.authenticate import authenticate_firebase
from springapi.models.firebase.client import get_firebase_users


def get_users(scheme, database_uri):
    if scheme == "firebase":
        if not admin.get_app():
            authenticate_firebase(database_uri)
        return get_firebase_users()
    else:
        raise ValueError(f"Unknown user database protocol: {scheme}")
