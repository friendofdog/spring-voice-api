import springapi.models.firebase.client as client
from springapi.models.exceptions import ValidationError
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


def _set_defaults(data: Dict[str, Any]) -> Dict[str, Any]:
    for field_name, field_settings in FIELDS.items():
        data.setdefault(field_name, field_settings["default"])
    return data


def _check_disallowed_fields(data: Dict[str, Any]) -> List[str]:
    disallowed = sorted([d for d in data if d not in FIELDS.keys()])
    return disallowed


def _check_required_fields(data: Dict[str, Any]) -> List[str]:
    required = [f for f in FIELDS if
                FIELDS[f]['isRequired'] is True]
    missing = sorted(list(set(required) - set(list(data.keys()))))
    return missing


def _check_type(data: Dict[str, Any]) -> List[str]:
    bad_types = sorted([d for d in data if d in FIELDS.keys() and
                        type(data[d]) is not FIELDS[d]['type']])
    return bad_types


def _validate_data(data: Dict[str, Any]) -> None:
    disallowed = _check_disallowed_fields(data)
    if disallowed:
        raise ValidationError(f'Not allowed: {", ".join(disallowed)}')

    missing = _check_required_fields(data)
    if missing:
        raise ValidationError(f'Missing: {", ".join(missing)}')

    bad_types = _check_type(data)
    if bad_types:
        type_errors = [f'{e} is {str(type(data[e]))}, should be '
                       f'{str(FIELDS[e]["type"])}.'
                       for e in bad_types]
        raise ValidationError(" ".join(type_errors))


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
        _validate_data(submission_data)
        populated = _set_defaults(submission_data)
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
        return Submission.from_json(response)

    @classmethod
    def create_submission(cls, data: Dict[str, Any]) -> "Submission":
        _validate_data(data)
        data = _set_defaults(data)

        response = client.add_entry(COLLECTION, data)
        result = response[data["id"]]
        result.setdefault("id", data["id"])
        return Submission.from_json(result)

    @classmethod
    def update_submission(
            cls, entry_id: str, data: Dict[str, Any]) -> "Submission":
        _validate_data(data)
        data = _set_defaults(data)

        response = client.update_entry(COLLECTION, data, entry_id)
        return Submission.from_json(response[entry_id])
