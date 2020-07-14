import re
from typing import Dict, Any, Optional, Union

from pydantic import BaseModel, Field, EmailStr, Extra, validator
from pydantic.validators import str_validator

from chalicelib.model import Reason


class PhoneNumberNotValidError(ValueError):
    """
    Error used to denote that a phone number was invalid
    """
    pass


class PhoneStr(str):
    """
    Custom type for validating strings as phone numbers
    """

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type='string', format='phone')

    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str]) -> str:
        # Verifies that a given string is a valid phone number
        match = re.match(r'^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$', value)
        valid = match is not None
        if not valid:
            raise PhoneNumberNotValidError('value is not a valid phone number')

        return value


def _clean_phone_number(phone_number: str) -> str:
    return re.sub(r'\D', '', phone_number)


class SenderCreationForm(BaseModel):
    alias: str = Field(..., min_length=1, max_length=50)
    phone: Optional[PhoneStr]
    email: EmailStr

    @validator('phone')
    def clean_phone(cls, value: Optional[PhoneStr]) -> Optional[str]:
        """
        Continued validation after phone validation that cleans phone string.
        This allows the string to be easily consumer throughout the application and we will only need to deal with
        a single phone format.

        :param value: The phone number string to clean
        :return: The cleaned phone number. None if no phone number was given
        """
        is_null = value is None
        return None if is_null else _clean_phone_number(value)

    class Config:
        anystr_strip_whitespace = True
        extra = Extra.forbid


class ContactMessageCreationForm(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    reason: Reason
    sender: SenderCreationForm

    class Config:
        anystr_strip_whitespace = True
        extra = Extra.forbid


class ContactMessageQuery(BaseModel):
    reason: Optional[str] = None
    archived: Optional[bool] = None
    responded: Optional[bool] = None
