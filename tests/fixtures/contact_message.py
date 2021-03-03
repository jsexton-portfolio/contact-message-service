from datetime import datetime
from typing import Dict, Any

import pytest

from chalicelib.model import Sender, Reader, ContactMessage
from chalicelib.service import ContactMessageFormPublished


@pytest.fixture
def sender() -> Sender:
    sender = Sender()
    sender.alias = 'test name'
    sender.ip = '123.456.8.5'
    sender.user_agent = 'chrome'
    sender.phone = '1234567890'
    sender.email = 'test@email.com'
    return sender


@pytest.fixture
def sender_json() -> Dict[str, Any]:
    return {
        'alias': 'test name',
        'ip': "123.456.8.5",
        'userAgent': 'chrome',
        'phone': '1234567890',
        'email': 'test@email.com'
    }


@pytest.fixture
def reader() -> Reader:
    reader = Reader()
    reader.user_id = '123'
    reader.flagged = True
    reader.time_updated = datetime.utcfromtimestamp(1000000000)
    return reader


@pytest.fixture
def reader_json() -> Dict[str, Any]:
    return {
        'userId': '123',
        'flagged': True,
        'timeUpdated': '2001-09-09T01:46:40'
    }


@pytest.fixture
def contact_message(sender: Sender, reader: Reader) -> ContactMessage:
    contact_message = ContactMessage()
    contact_message.id = '5eeaa9f461cf5af67b7feaae'
    contact_message.message = 'test message'
    contact_message.sender = sender
    contact_message.readers = [reader]
    contact_message.time_updated = datetime.utcfromtimestamp(1000000000)
    contact_message.time_created = datetime.utcfromtimestamp(1000000000)

    return contact_message


@pytest.fixture
def contact_message_json() -> Dict[str, Any]:
    return {
        'id': '5eeaa9f461cf5af67b7feaae',
        'message': 'test message',
        'archived': False,
        'responded': False,
        'readers': [
            {
                'userId': '123',
                'flagged': True,
                'timeUpdated': '2001-09-09T01:46:40'
            }
        ],
        'sender': {
            'alias': 'test name',
            'ip': "123.456.8.5",
            'userAgent': 'chrome',
            'phone': '1234567890',
            'email': 'test@email.com'
        },
        'timeUpdated': '2001-09-09T01:46:40',
        'timeCreated': '2001-09-09T01:46:40'
    }


@pytest.fixture
def sender_creation_form_json() -> Dict[str, Any]:
    return {
        'alias': 'test',
        'phone': '1234567890',
        'email': 'test@test.com'
    }


@pytest.fixture
def message_creation_form_json(sender_creation_form_json) -> Dict[str, Any]:
    return {
        'message': 'message',
        'reason': 'business',
        'sender': sender_creation_form_json
    }


@pytest.fixture
def message_form_published() -> ContactMessageFormPublished:
    return ContactMessageFormPublished('123', '123')


@pytest.fixture
def message_form_published_json() -> Dict[str, Any]:
    return {
        'contactMessageId': '123',
        'snsMessageId': '123'
    }
