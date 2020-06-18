import pytest

from chalicelib.service import ContactMessageService


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
    assert expected == ContactMessageService._clean_phone_number(phone)
