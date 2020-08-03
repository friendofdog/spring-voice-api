import springapi.models.firebase.client as client


def get_submissions():
    return client.get_collection('submissions')


def get_submission(entry_id):
    submission = client.get_entry('submissions', entry_id)
    status = '200 OK' if submission else '404 NOT FOUND'
    response = submission if submission \
        else f'Entry with id {entry_id} not found in submissions'
    return response, status


class Submission:

    def __init__(self):
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
        errors = []
        missing = self._check_required_fields(data)
        if missing:
            errors.append(f'Missing: {", ".join(missing)}')

        bad_types = self._check_type(data)
        if bad_types:
            type_errors = [f'{e} is {type(data[e]).__name__}, should be '
                           f'{self.fields[e]["type"].__name__}.'
                           for e in bad_types]
            errors.append(f'Fields with type errors: '
                          f'{" ".join(type_errors)}')

        return errors

    def create_submission(self, data):
        invalid = self._validate_data(data)
        if invalid:
            return '\r\n'.join(invalid), '400 BAD REQUEST'
        else:
            response, status = client.add_entry('submission', data)
            if response and status == '201 CREATED':
                return response, status
            else:
                return 'An error occured:\r\n' \
                       f'{response}', status

    def update_submission(self, data, entry_id):
        invalid = self._validate_data(data)
        if invalid:
            return '\r\n'.join(invalid), '400 BAD REQUEST'
        else:
            response, status = client.update_entry(
                'submission', data, entry_id)
            if response and status == '200 OK':
                return response, status
            else:
                return 'An error occured:\r\n' \
                       f'{response}', status
