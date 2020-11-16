import springapi.models.firebase.client as client
from springapi.exceptions import ValidationError
from springapi.models.helpers import ApiObjectModel
from typing import Dict, List, Any


COLLECTION = "tokens"


class Token(ApiObjectModel):

    _fields = {
        'token': {'isRequired': True, 'type': str, 'default': ''}
    }

    def __init__(self, field_data, **fields):
        super().__init__(field_data, **fields)
        self.fields = field_data

    @classmethod
    def get_tokens(cls) -> List["ApiObjectModel"]:
        response = client.get_collection(COLLECTION)
        tokens = []
        for result_id, result in response.items():
            try:
                tokens.append(Token.from_json(result))
            except ValidationError:
                continue
        return tokens

    @classmethod
    def create_token(cls, data: Dict[str, Any]) -> "ApiObjectModel":
        pass

    @classmethod
    def delete_token(cls, token: str) -> "ApiObjectModel":
        pass
