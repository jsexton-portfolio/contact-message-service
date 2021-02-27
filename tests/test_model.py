from datetime import datetime

import pytest

from chalicelib.model import Reason, Sender, Reader, ContactMessage


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
def reader() -> Reader:
    reader = Reader()
    reader.user_id = '123'
    reader.flagged = True
    reader.time_updated = datetime.utcfromtimestamp(1000000000)
    return reader


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


@pytest.mark.parametrize('reason', [
    'business',
    'BusINEss',
    'other',
    'OTHeR'
])
def test_reason_is_case_insensitive(reason):
    Reason(reason)


def test_sender_is_correctly_serialized(sender: Sender):
    json = sender.__getstate__()
    assert json == {
        'alias': 'test name',
        'ip': "123.456.8.5",
        'userAgent': 'chrome',
        'phone': '1234567890',
        'email': 'test@email.com'
    }


def test_reader_is_correctly_serialized(reader: Reader):
    json = reader.__getstate__()
    assert json == {
        'userId': '123',
        'flagged': True,
        'timeUpdated': '2001-09-09T01:46:40'
    }


def test_contact_message_is_correctly_serialized(contact_message: ContactMessage):
    json = contact_message.__getstate__()
    assert json == {
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
