import json
from datetime import datetime
from enum import Enum
from typing import Sequence

from mongoengine import BooleanField
from mongoengine import DateTimeField
from mongoengine import EmailField
from mongoengine import EmbeddedDocumentField
from mongoengine import ListField
from mongoengine import ReferenceField
from mongoengine import StringField
from mongoengine_goodjson import Document, EmbeddedDocument

from pyocle.serialization import CamelCaseAttributesMixin


class Reason(Enum):
    """
    Represents all possible reasons a message was constructed
    """
    BUSINESS = 'business'
    QUESTION = 'question'
    FEEDBACK = 'feedback'
    OTHER = 'other'

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.name.lower() == value.lower():
                return member


class Sender(EmbeddedDocument):
    """
    Represents sender document in mongo
    """
    alias = StringField(min_length=1, max_length=50, required=True)
    phone = StringField(min_length=6, max_length=15)
    email = EmailField(required=True)
    ip = StringField(required=True)
    user_agent = StringField(db_field='userAgent', required=True)

    def __getstate__(self):
        return json.loads(self.to_json())


class Reader(Document):
    """
    Represents reader document in mongo
    """
    id = StringField(required=True)
    flagged = BooleanField(default=False, required=True)
    time_updated = DateTimeField(db_field='timeUpdated', default=datetime.utcnow, required=True)

    def __getstate__(self):
        return json.loads(self.to_json())


class ReaderCollection(CamelCaseAttributesMixin):
    """
    Container for list of readers.
    Provides meta information about the list of readers.
    Will be most commonly used in responses
    """

    def __init__(self, readers: Sequence[Reader]):
        self.count = len(readers)
        self.reader_list = readers


class ContactMessage(Document):
    """
    Represents contact message document in mongo
    """
    message = StringField(min_length=1, max_length=2000, required=True)
    reason = StringField(enum=Reason, required=True)
    archived = BooleanField(default=False, required=True)
    responded = BooleanField(default=False, required=True)
    sender = EmbeddedDocumentField(document_type=Sender, required=True)
    readers = ListField(ReferenceField(Reader))
    time_created = DateTimeField(db_field='timeCreated', default=datetime.utcnow, required=True)
    time_updated = DateTimeField(db_field='timeUpdated', default=datetime.utcnow, required=True)

    def __getstate__(self):
        return json.loads(self.to_json(follow_reference=True))


class ContactMessageCollection(CamelCaseAttributesMixin):
    """
    Container for list of contact messages.
    Provides meta information about the list of contact messages.
    Will be most commonly used in responses
    """

    def __init__(self, contact_messages: Sequence[ContactMessage]):
        self.count = len(contact_messages)
        self.contact_messages = contact_messages
