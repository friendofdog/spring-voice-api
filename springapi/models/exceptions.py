class CollectionNotFound(Exception):

    def __init__(self, collection):
        self.message = f'Collection {collection} not found'

    def error_response_body(self):
        return {'error': self.message}


class EntryAlreadyExists(Exception):

    def __init__(self, entry_id, collection):
        self.message = f'{entry_id} already exists in {collection}'

    def error_response_body(self):
        return {'error': self.message}


class EntryNotFound(Exception):

    def __init__(self, entry_id, collection):
        self.message = f'{entry_id} was not found in {collection}'

    def error_response_body(self):
        return {'error': self.message}


class ServerError(Exception):

    def __init__(self, message, code):
        self.message = message
        self.code = code

    def error_response_body(self):
        return {'error': self.message, 'code': self.code}, self.code


class ValidationError(Exception):

    def __init__(self, message):
        self.message = message

    def error_response_body(self):
        return {'error': self.message}
