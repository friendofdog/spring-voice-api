from springapi.exceptions import ValidationError
from springapi.models.firebase import client
from springapi.models.helpers import ApiObjectModel
from typing import List


COLLECTION = "users"


class User(ApiObjectModel):

    _fields = {
        'id': {'isRequired': True, 'type': str, 'default': ''},
        'email': {'isRequired': True, 'type': str, 'default': ''},
        'token': {'isRequired': False, 'type': str, 'default': ''}
    }

    def __init__(self, field_data, **fields):
        super().__init__(field_data, **fields)
        self.fields = field_data

    @classmethod
    def get_users(cls) -> List["ApiObjectModel"]:
        response = client.get_collection(COLLECTION)
        users = []
        for result_id, result in response.items():
            result["id"] = result_id
            try:
                users.append(User.from_json(result))
            except ValidationError:
                continue
        return users
