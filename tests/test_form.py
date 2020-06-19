import copy
from typing import Dict, Any

import jsonpickle
import pytest

from chalicelib.form import resolve_form, SenderCreationForm, ContactMessageCreationForm, FormValidationError, \
    _clean_phone_number


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
        'message': 'This is a test message that only need to be longer than 50 characters long.'
                   ' Lets make this just a bit longer so that the database does not complain to us.',
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
    contact_creation_form['alias'] = ''
    return contact_creation_form


@pytest.fixture
def empty_sender_phone_form(contact_creation_form):
    contact_creation_form['phone'] = ''
    return contact_creation_form


@pytest.fixture
def null_sender_phone_form(contact_creation_form):
    contact_creation_form['phone'] = None
    return contact_creation_form


@pytest.fixture
def get_fixture(request):
    def _get_fixture_by_name(name):
        return request.getfixturevalue(name)

    return _get_fixture_by_name


@pytest.fixture
def valid_form_json(contact_creation_form) -> str:
    return jsonpickle.dumps(contact_creation_form, unpicklable=False)


@pytest.fixture
def valid_form_bytes(valid_form_json) -> bytes:
    return bytes(valid_form_json, 'utf-8')


def test_resolve_form_when_form_is_valid(contact_creation_form):
    contact_creation_form = resolve_form(contact_creation_form, ContactMessageCreationForm)
    assert contact_creation_form is not None


def test_resolve_form_returns_resolved_form__when_given_valid_string(valid_form_json):
    contact_creation_form = resolve_form(valid_form_json, ContactMessageCreationForm)
    assert contact_creation_form is not None


def test_resolve_form_returns_resolved_form_when_given_valid_bytes(valid_form_bytes):
    contact_creation_form = resolve_form(valid_form_bytes, ContactMessageCreationForm)
    assert contact_creation_form is not None


@pytest.mark.parametrize('data', [
    None,
    '',
    '{',
    '123'
])
def test_resolve_form_raises_form_validation_error_when_given_invalid_or_no_json(data):
    with pytest.raises(FormValidationError) as exception_info:
        resolve_form(data, ContactMessageCreationForm)

    exception = exception_info.value
    assert exception.message == 'Form could not be validated due to given json not existing or being valid'
    assert exception.schema is not None
    assert len(exception.error_details) == 1


# See https://docs.pytest.org/en/latest/proposals/parametrize_with_fixtures.html
# See https://github.com/pytest-dev/pytest/issues/349
@pytest.mark.parametrize('fixture_name,error_count', [
    pytest.param('null_reason_form', 1),
    pytest.param('unsupported_reason_form', 1),
    pytest.param('null_message_form', 1),
    pytest.param('empty_message_form', 1),
    pytest.param('empty_sender_alias_form', 1),
    pytest.param('empty_sender_phone_form', 1),
    pytest.param('null_sender_phone_form', 1),
])
def test_resolve_form_when_form_is_invalid(get_fixture, fixture_name, error_count):
    form = get_fixture(fixture_name)

    with pytest.raises(FormValidationError) as exception_info:
        resolve_form(form, ContactMessageCreationForm)

    exception = exception_info.value
    assert exception.message == 'Form was not validated successfully'
    assert len(exception.error_details) == error_count


def test_resolve_form_raises_value_error_when_given_unsupported_form_type(contact_creation_form):
    with pytest.raises(ValueError) as exception_info:
        resolve_form(contact_creation_form, SenderCreationForm)

    expected_message = 'Unsupported form type: SenderCreationForm'
    assert expected_message in str(exception_info.value)


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
