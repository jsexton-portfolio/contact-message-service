from typing import Dict, Any

import jsonpickle
import pytest

from chalicelib.form import resolve_form, SenderCreationForm, ContactMessageCreationForm, FormValidationError


@pytest.fixture
def valid_sender() -> Dict[str, Any]:
    return {
        'alias': 'test',
        'phone': '1234567890',
        'email': 'test@test.com'
    }


@pytest.fixture
def valid_form(valid_sender) -> Dict[str, Any]:
    return {
        'message': 'This is a test message that only need to be longer than 50 characters long.'
                   ' Lets make this just a bit longer so that the database does not complain to us.',
        'reason': 'business',
        'sender': valid_sender
    }


@pytest.fixture
def valid_form_json(valid_form) -> str:
    return jsonpickle.dumps(valid_form, unpicklable=False)


@pytest.fixture
def valid_form_bytes(valid_form_json) -> bytes:
    return bytes(valid_form_json, 'utf-8')


def test_resolve_form_when_form_is_valid(valid_form):
    contact_creation_form = resolve_form(valid_form, ContactMessageCreationForm)
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


# NOTE: In the future will need to make sure the removal of whitespace does not affect validation of expected lengths.

# This currently does not work but will work soon.
# See https://docs.pytest.org/en/latest/proposals/parametrize_with_fixtures.html
# See https://github.com/pytest-dev/pytest/issues/349
# @pytest.mark.parametrize('form,error_count', [
#     (small_message_form, 1),
#     (unsupported_reason_form, 1),
#     (sender_alias_non_existent_form, 1),
#     (sender_alias_too_large_form, 1),
# ])
# def test_resolve_form_when_form_is_invalid(form, error_count):
#     with pytest.raises(FormValidationError) as exception_info:
#         resolve_form(form, ContactMessageCreationForm)
#
#     exception = exception_info.value
#     assert exception.message == 'Form was not validated successfully'
#     assert len(exception.error_details) == error_count


def test_resolve_form_raises_value_error_when_given_unsupported_form_type(valid_form):
    with pytest.raises(ValueError) as exception_info:
        resolve_form(valid_form, SenderCreationForm)

    expected_message = 'Unsupported form type: SenderCreationForm'
    assert expected_message in str(exception_info.value)
