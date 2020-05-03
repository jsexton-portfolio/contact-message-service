import pytest

from chalicelib.form import resolve_form, SenderCreationForm, ContactMessageCreationForm


@pytest.fixture
def valid_sender():
    return {
        'alias': 'test',
        'phone': '1234567890',
        'email': 'test@test.com'
    }


@pytest.fixture
def valid_form(valid_sender):
    return {
        'message': 'This is a test message that only need to be longer than 50 characters long.'
                   ' Lets make this just a bit longer so that the database does not complain to us.',
        'reason': 'business',
        'sender': valid_sender
    }


def test_resolve_form_when_form_is_valid(valid_form):
    contact_creation_form = resolve_form(valid_form, ContactMessageCreationForm)
    assert contact_creation_form is not None


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
