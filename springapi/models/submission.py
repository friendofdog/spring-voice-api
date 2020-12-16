import springapi.models.firebase.client as client
from springapi.exceptions import ValidationError
from springapi.models.helpers import (
    ApiObjectModel, create_uid, validate_data, set_defaults)
from typing import Dict, List, Any


COLLECTION = 'submissions'


class Submission(ApiObjectModel):

    _fields = {
        'allowSharing': {'isRequired': False, 'type': bool, 'default': False},
        'allowSNS': {'isRequired': False, 'type': bool, 'default': False},
        'isApproved': {'isRequired': False, 'type': bool, 'default': False},
        'location': {'isRequired': True, 'type': str, 'default': ''},
        'message': {'isRequired': True, 'type': str, 'default': ''},
        'name': {'isRequired': True, 'type': str, 'default': ''},
        'id': {'isRequired': True, 'type': str, 'default': ''}
    }

    def __init__(self, field_data, **fields):
        super().__init__(field_data, **fields)
        self.fields = field_data

    @classmethod
    def get_submissions(cls) -> List["ApiObjectModel"]:
        response = client.get_collection(COLLECTION)
        submissions = []
        for result_id, result in response.items():
            result["id"] = result_id
            try:
                submissions.append(Submission.from_json(result))
            except ValidationError:
                continue
        return submissions

    @classmethod
    def get_submission(cls, entry_id: str) -> "ApiObjectModel":
        response = client.get_entry(COLLECTION, entry_id)
        response["id"] = entry_id
        submission = Submission.from_json(response)
        return submission

    @classmethod
    def create_submission(cls, data: Dict[str, Any]) -> "ApiObjectModel":
        data["id"] = create_uid()
        validate_data(data, cls._fields)
        data = set_defaults(data, cls._fields)

        response = client.add_entry(COLLECTION, data.copy())
        result = response[data["id"]]
        result.setdefault("id", data["id"])
        return Submission.from_json(result)

    @classmethod
    def update_submission(
            cls, entry_id: str, data: Dict[str, Any]) -> "ApiObjectModel":
        data["id"] = entry_id
        validate_data(data, cls._fields)
        data = set_defaults(data, cls._fields)

        response = client.update_entry(COLLECTION, data.copy(), entry_id)
        return response
