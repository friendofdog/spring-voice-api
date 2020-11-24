import springapi.models.firebase.client as client

from typing import Dict, List, Any

from springapi.exceptions import ValidationError
from springapi.models.helpers import (
    ApiObjectModel, create_uid, set_defaults, validate_data)


COLLECTION = "tokens"


class Token(ApiObjectModel):

    _fields = {
        "id": {"isRequired": True, "type": str, "default": ""},
        "token": {"isRequired": True, "type": str, "default": ""}
    }

    def __init__(self, field_data, **fields):
        super().__init__(field_data, **fields)
        self.fields = field_data

    @classmethod
    def get_tokens(cls) -> List["ApiObjectModel"]:
        response = client.get_collection(COLLECTION)
        tokens = []
        for result_id, result in response.items():
            result["id"] = result_id
            try:
                tokens.append(Token.from_json(result))
            except ValidationError:
                continue
        return tokens

    @classmethod
    def create_token(cls, data: Dict[str, Any]) -> "ApiObjectModel":
        data["id"] = create_uid()
        validate_data(data, cls._fields)
        data = set_defaults(data, cls._fields)

        response = client.add_entry(COLLECTION, data.copy())
        result = response[data["id"]]
        result.setdefault("id", data["id"])
        return Token.from_json(result)

    @classmethod
    def delete_token(cls, token: str) -> "ApiObjectModel":
        pass
