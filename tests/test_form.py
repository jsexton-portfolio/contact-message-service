import pytest
from pyocle.form import resolve_form, FormValidationError

from chalicelib.form import ContactMessageCreationForm, _clean_phone_number


@pytest.fixture
def unsupported_reason_form(message_creation_form_json):
    message_creation_form_json['reason'] = 'invalid'
    return message_creation_form_json


@pytest.fixture
def null_reason_form(message_creation_form_json):
    message_creation_form_json['reason'] = None
    return message_creation_form_json


@pytest.fixture
def unsupported_reason_form(message_creation_form_json):
    message_creation_form_json['reason'] = 'invalid'
    return message_creation_form_json


@pytest.fixture
def null_message_form(message_creation_form_json):
    message_creation_form_json['message'] = None
    return message_creation_form_json


@pytest.fixture
def empty_message_form(message_creation_form_json):
    message_creation_form_json['message'] = ''
    return message_creation_form_json


@pytest.fixture
def empty_sender_alias_form(message_creation_form_json):
    message_creation_form_json['sender']['alias'] = ''
    return message_creation_form_json


@pytest.fixture
def empty_sender_phone_form(message_creation_form_json):
    message_creation_form_json['sender']['phone'] = ''
    return message_creation_form_json


# See https://docs.pytest.org/en/latest/proposals/parametrize_with_fixtures.html
# See https://github.com/pytest-dev/pytest/issues/349
@pytest.mark.parametrize('fixture_name,error_count', [
    ('null_reason_form', 1),
    ('unsupported_reason_form', 1),
    ('null_message_form', 1),
    ('empty_message_form', 1),
    ('empty_sender_alias_form', 1),
    ('empty_sender_phone_form', 1),
])
def test_resolve_form_when_form_is_invalid(get_fixture, fixture_name, error_count):
    form = get_fixture(fixture_name)

    with pytest.raises(FormValidationError) as exception_info:
        resolve_form(form, ContactMessageCreationForm)

    exception = exception_info.value
    assert exception.message == 'Form was not validated successfully'
    assert len(exception.errors) == error_count


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
