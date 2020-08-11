import springapi.models.firebase.client as client
from springapi.models.exceptions import ValidationError


class Submission:

    def __init__(self):
        self.collection = 'submissions'
        self.fields = {
            'name': {'isRequired': True, 'type': str},
            'message': {'isRequired': True, 'type': str},
            'location': {'isRequired': True, 'type': str}
        }

    def _check_required_fields(self, data):
        required = [f for f in self.fields if
                    self.fields[f]['isRequired'] is True]
        missing = sorted(list(set(required) - set(list(data.keys()))))
        return missing

    def _check_type(self, data):
        bad_types = sorted([d for d in data if d in self.fields.keys() and
                            type(data[d]) is not self.fields[d]['type']])
        return bad_types

    def _validate_data(self, data):
        missing = self._check_required_fields(data)
        if missing:
            raise ValidationError(f'Missing: {", ".join(missing)}')

        bad_types = self._check_type(data)
        if bad_types:
            type_errors = [f'{e} is {type(data[e]).__name__}, should be '
                           f'{self.fields[e]["type"].__name__}.'
                           for e in bad_types]
            raise ValidationError(" ".join(type_errors))

    def get_submissions(self):
        response = client.get_collection(self.collection)
        return response

    def get_submission(self, entry_id):
        response = client.get_entry(self.collection, entry_id)
        return response

    def create_submission(self, data):
        invalid = self._validate_data(data)
        if invalid:
            raise ValidationError('\r\n'.join(invalid))

        response = client.add_entry(self.collection, data)
        return response

    def update_submission(self, entry_id, data):
        invalid = self._validate_data(data)
        if invalid:
            raise ValidationError('\r\n'.join(invalid))

        response = client.update_entry(self.collection, data, entry_id)
        return response
