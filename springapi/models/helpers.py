import base64
import uuid
from springapi.exceptions import ValidationError
from typing import Dict, List, Any


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


def _check_type(data: Dict[str, Any], fields) -> List[str]:
    bad_types = sorted([d for d in data if d in fields.keys() and
                        type(data[d]) is not fields[d]['type']])
    return bad_types


def validate_data(data: Dict[str, Any], fields) -> None:
    disallowed = _check_disallowed_fields(data, fields)
    if disallowed:
        raise ValidationError(f'Not allowed: {", ".join(disallowed)}')

    missing = _check_required_fields(data, fields)
    if missing:
        raise ValidationError(f'Missing: {", ".join(missing)}')

    bad_types = _check_type(data, fields)
    if bad_types:
        type_errors = [f'{e} is {str(type(data[e]))}, should be '
                       f'{str(fields[e]["type"])}.'
                       for e in bad_types]
        raise ValidationError(" ".join(type_errors))
