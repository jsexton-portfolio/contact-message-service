from typing import Dict, Any

import pytest

from chalicelib.model import Reason, Sender, Reader, ContactMessage, ReaderCollection


@pytest.mark.parametrize('reason', [
    'business',
    'BusINEss',
    'other',
    'OTHeR'
])
def test_reason_is_case_insensitive(reason):
    Reason(reason)


def test_sender_is_correctly_serialized(sender: Sender, sender_json: Dict[str, Any]):
    json = sender.__getstate__()
    assert json == sender_json


def test_reader_is_correctly_serialized(reader: Reader, reader_json: Dict[str, Any]):
    json = reader.__getstate__()
    assert json == reader_json


def test_contact_message_is_correctly_serialized(contact_message: ContactMessage, contact_message_json: Dict[str, Any]):
    json = contact_message.__getstate__()
    assert json == contact_message_json


def test_reader_collection_fields_are_calculated_correctly_without_user_id(reader: Reader):
    readers = [reader]
    collection = ReaderCollection(readers)

    assert collection.__dict__ == {
        'count': 1,
        'read_by_any': True,
        'flagged_by_any': True,
        'read_by_you': None,
        'flagged_by_you': None,
        'reader_list': readers
    }


def test_reader_collection_fields_are_calculated_correctly_with_known_id(reader: Reader):
    readers = [reader]
    collection = ReaderCollection(readers, '123')

    assert collection.__dict__ == {
        'count': 1,
        'read_by_any': True,
        'flagged_by_any': True,
        'read_by_you': True,
        'flagged_by_you': True,
        'reader_list': readers
    }


def test_reader_collection_fields_are_calculated_correctly_with_unknown_id(reader: Reader):
    readers = [reader]
    collection = ReaderCollection(readers, 'unknown id')

    assert collection.__dict__ == {
        'count': 1,
        'read_by_any': True,
        'flagged_by_any': True,
        'read_by_you': False,
        'flagged_by_you': False,
        'reader_list': readers
    }
