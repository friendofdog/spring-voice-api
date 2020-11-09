from springapi.models.helpers import ApiObjectModel
from springapi.models.firebase import client


class Email(ApiObjectModel):

    @classmethod
    def get_authorized_emails(cls) -> "ApiObjectModel":
        emails = client.get_email_addresses()
        return emails
