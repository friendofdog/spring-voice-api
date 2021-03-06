import base64
import uuid
from springapi.exceptions import ValidationError
from typing import Dict, List, Any, Tuple


class ApiObjectModel:

    _fields: Dict[str, Any] = {}

    def __init__(self, field_data, **fields):
        self.fields = field_data
        for f in fields:
            setattr(self, f, fields[f])

    def __eq__(self, other):
        if not isinstance(other, ApiObjectModel):
            return False
        return self.to_json() == other.to_json()

    @classmethod
    def from_json(cls, user_data: Dict[str, Any]) -> "ApiObjectModel":
        validate_data(user_data, cls._fields)
        populated = set_defaults(user_data, cls._fields)
        return cls(cls._fields, **populated)

    def to_json(self):
        json = dict([(k, getattr(self, k)) for k in self.fields.keys()])
        return json


def create_uid():
    raw_uid = uuid.uuid4().bytes
    uid_base32 = \
        base64.b32encode(raw_uid).decode('ascii').rsplit("=")[0].lower()
    return uid_base32


def set_defaults(data: Dict[str, Any], fields) -> Dict[str, Any]:
    for field_name, field_settings in fields.items():
        data.setdefault(field_name, field_settings["default"])
    return data


def _check_disallowed_fields(data: Dict[str, Any], fields) -> List[str]:
    disallowed = sorted([d for d in data if d not in fields.keys()])
    return disallowed


def _check_required_fields(data: Dict[str, Any], fields) -> List[str]:
    required = [f for f in fields if
                fields[f]['isRequired'] is True]
    missing = sorted(list(set(required) - set(list(data.keys()))))
    return missing


def _check_type(data: Dict[str, Any], fields) -> List[Tuple[str, str, str]]:
    bad_types = sorted([(d, str(type(data[d])), str(fields[d]["type"]))
                        for d in data if d in fields.keys() and
                        type(data[d]) is not fields[d]['type']])
    return bad_types


def validate_data(data: Dict[str, Any], fields) -> None:
    disallowed = _check_disallowed_fields(data, fields)
    if disallowed:
        raise ValidationError(disallowed, "not_allowed")

    missing = _check_required_fields(data, fields)
    if missing:
        raise ValidationError(missing, "missing")

    bad_types = _check_type(data, fields)
    if bad_types:
        raise ValidationError(bad_types, "type")
