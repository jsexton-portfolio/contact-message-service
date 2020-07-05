import copy
from typing import Dict, Any

import pytest
from pyocle.error import FormValidationError
from pyocle.form import resolve_form

from chalicelib.form import ContactMessageCreationForm, _clean_phone_number


@pytest.fixture
def sender_creation_form() -> Dict[str, Any]:
    valid_sender_form = {
        'alias': 'test',
        'phone': '1234567890',
        'email': 'test@test.com'
    }

    return copy.deepcopy(valid_sender_form)


@pytest.fixture
def contact_creation_form(sender_creation_form) -> Dict[str, Any]:
    valid_form = {
        'message': 'message',
        'reason': 'business',
        'sender': sender_creation_form
    }

    return copy.deepcopy(valid_form)


@pytest.fixture
def unsupported_reason_form(contact_creation_form):
    contact_creation_form['reason'] = 'invalid'
    return contact_creation_form


@pytest.fixture
def null_reason_form(contact_creation_form):
    contact_creation_form['reason'] = None
    return contact_creation_form


@pytest.fixture
def unsupported_reason_form(contact_creation_form):
    contact_creation_form['reason'] = 'invalid'
    return contact_creation_form


@pytest.fixture
def null_message_form(contact_creation_form):
    contact_creation_form['message'] = None
    return contact_creation_form


@pytest.fixture
def empty_message_form(contact_creation_form):
    contact_creation_form['message'] = ''
    return contact_creation_form


@pytest.fixture
def empty_sender_alias_form(contact_creation_form):
    contact_creation_form['sender']['alias'] = ''
    return contact_creation_form


@pytest.fixture
def empty_sender_phone_form(contact_creation_form):
    contact_creation_form['sender']['phone'] = ''
    return contact_creation_form


@pytest.fixture
def get_fixture(request):
    def _get_fixture_by_name(name):
        return request.getfixturevalue(name)

    return _get_fixture_by_name


# See https://docs.pytest.org/en/latest/proposals/parametrize_with_fixtures.html
# See https://github.com/pytest-dev/pytest/issues/349
@pytest.mark.parametrize('fixture_name,error_count', [
    pytest.param('null_reason_form', 1),
    pytest.param('unsupported_reason_form', 1),
    pytest.param('null_message_form', 1),
    pytest.param('empty_message_form', 1),
    pytest.param('empty_sender_alias_form', 1),
    pytest.param('empty_sender_phone_form', 1),
])
def test_resolve_form_when_form_is_invalid(get_fixture, fixture_name, error_count):
    form = get_fixture(fixture_name)

    with pytest.raises(FormValidationError) as exception_info:
        resolve_form(form, ContactMessageCreationForm)

    exception = exception_info.value
    assert exception.message == 'Form was not validated successfully'
    assert len(exception.error_details) == error_count


@pytest.mark.parametrize('phone,expected', [
    ('1234567890', '1234567890'),
    ('123 456 7890', '1234567890'),
    ('123-456-7890', '1234567890'),
    ('(123)4567890', '1234567890'),
    ('(123) 456-7890', '1234567890'),
    ('(123) 456-7890', '1234567890'),
    ('(123)-456-7890', '1234567890')
])
def test_clean_phone_number_correctly_cleans_given_string(phone: str, expected: str):
    assert expected == _clean_phone_number(phone)
