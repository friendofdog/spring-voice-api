import springapi.models.firebase.client as client


def check_required_fields(fields, data):
    required = [f for f in fields if fields[f]['isRequired'] is True]
    missing = sorted(list(set(required) - set(list(data.keys()))))
    return missing


def check_type(fields, data):
    bad_types = sorted([d for d in data if d in fields.keys() and
                        type(data[d]) is not fields[d]['type']])
    return bad_types


def get_submissions():
    return client.get_collection('submissions')


def get_submission(entry_id):
    submission = client.get_entry('submissions', entry_id)
    status = '200 OK' if submission else '404 NOT FOUND'
    response = submission if submission\
        else f'Entry with id {entry_id} not found in submissions'
    return response, status


def create_submission(data):
    fields = {
        'name': {'isRequired': True, 'type': str},
        'message': {'isRequired': True, 'type': str},
        'location': {'isRequired': True, 'type': str}
    }

    missing = check_required_fields(fields, data)
    if missing:
        return f'Missing: {", ".join(missing)}', '400 BAD REQUEST'

    bad_types = check_type(fields, data)
    if bad_types:
        type_errors = [f'{e} is {type(data[e]).__name__} should be '
                       f'{fields[e]["type"].__name__}'
                       for e in bad_types]
        return f'Fields with type errors: {", ".join(type_errors)}', \
               '400 BAD REQUEST'

    response, status = client.add_entry('submission', data)
    if response and status == '201 CREATED':
        return response, status
    else:
        return 'A server error occured', '500 INTERNAL SERVER ERROR'


def update_submission():
    pass
