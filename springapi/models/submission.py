import springapi.models.firebase.client as client
from springapi.exceptions import ValidationError
from springapi.models.helpers import create_uid, set_defaults, validate_data
from typing import Dict, List, Any


COLLECTION = 'submissions'

FIELDS = {
    'allowSharing': {'isRequired': False, 'type': bool, 'default': False},
    'allowSNS': {'isRequired': False, 'type': bool, 'default': False},
    'isApproved': {'isRequired': False, 'type': bool, 'default': False},
    'location': {'isRequired': True, 'type': str, 'default': ''},
    'message': {'isRequired': True, 'type': str, 'default': ''},
    'name': {'isRequired': True, 'type': str, 'default': ''},
    'id': {'isRequired': True, 'type': str, 'default': ''}
}


class Submission:

    def __init__(
            self, identifier, name, message, location, is_approved, allow_sns,
            allow_sharing):
        self.identifier = identifier
        self.name = name
        self.message = message
        self.location = location
        self.is_approved = is_approved
        self.allow_sns = allow_sns
        self.allow_sharing = allow_sharing

    @classmethod
    def from_json(cls, submission_data: Dict[str, Any]) -> "Submission":
        validate_data(submission_data, FIELDS)
        populated = set_defaults(submission_data, FIELDS)
        return cls(
            identifier=populated["id"],
            name=populated["name"],
            message=populated["message"],
            location=populated["location"],
            is_approved=populated["isApproved"],
            allow_sns=populated["allowSNS"],
            allow_sharing=populated["allowSharing"])

    def to_json(self):
        return {
            "id": self.identifier,
            "name": self.name,
            "message": self.message,
            "location": self.location,
            "allowSNS": self.allow_sns,
            "allowSharing": self.allow_sharing,
            "isApproved": self.is_approved
        }

    def __eq__(self, other):
        if not isinstance(other, Submission):
            return False
        return self.to_json() == other.to_json()

    @classmethod
    def get_submissions(cls) -> List["Submission"]:
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
    def get_submission(cls, entry_id: str) -> "Submission":
        response = client.get_entry(COLLECTION, entry_id)
        response["id"] = entry_id
        try:
            submission = Submission.from_json(response)
        except ValidationError as err:
            raise ValueError(err)
        return submission

    @classmethod
    def create_submission(cls, data: Dict[str, Any]) -> "Submission":
        data["id"] = create_uid()
        validate_data(data, FIELDS)
        data = set_defaults(data, FIELDS)

        response = client.add_entry(COLLECTION, data.copy())
        result = response[data["id"]]
        result.setdefault("id", data["id"])
        return Submission.from_json(result)

    @classmethod
    def update_submission(
            cls, entry_id: str, data: Dict[str, Any]) -> "Submission":
        data["id"] = entry_id
        validate_data(data, FIELDS)
        data = set_defaults(data, FIELDS)

        response = client.update_entry(COLLECTION, data.copy(), entry_id)
        return response
