import json
import re
from typing import TypeVar, Type, Dict, Any, Optional, Sequence, Union

from pydantic import BaseModel, Field, ValidationError, EmailStr, Extra
from pydantic.validators import str_validator

from chalicelib.model import Reason
from chalicelib.response import ErrorDetail, FieldErrorDetail


class FormError(Exception):
    """
    Any error that may be raised while handling a form
    """
    pass


class PhoneNumberNotValidError(ValueError):
    """
    Error used to denote that a phone number was invalid
    """
    pass


class FormValidationError(FormError):
    """
    Error raised when an incoming request form is invalid
    """

    def __init__(self,
                 error_details: Optional[Sequence[ErrorDetail]] = None,
                 message: str = None,
                 schema: Dict[str, Any] = None):
        self.error_details = error_details or []
        self.message = message or 'Form was not validated successfully'
        self.schema = schema


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


class SenderCreationForm(BaseModel):
    alias: str = Field(..., min_length=1, max_length=50)
    phone: Optional[PhoneStr]
    email: EmailStr

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


T = TypeVar('T')
SUPPORTED_FORM_TYPES = {
    ContactMessageCreationForm,
}


def resolve_form(data: Union[str, bytes, Dict[str, Any]], form_type: Type[T]) -> T:
    """
    Resolves a form from given type and json in the form of a dict. Validates form against given json
    and raises FormValidationError if form is invalid.

    :param data: The json that will be used to build the form. This data can be given in
     the form of string, bytes or dictionary.
    :param form_type: The form type to resolve
    :return: The resolved form
    """

    if form_type not in SUPPORTED_FORM_TYPES:
        raise ValueError(f'Unsupported form type: {form_type.__name__}')

    try:
        if isinstance(data, (str, bytes)):
            data = json.loads(data)

        return form_type(**data)
    except ValidationError as ex:
        error_details = _build_error_details(ex.errors())
        raise FormValidationError(error_details=error_details, schema=form_type.schema())
    except (TypeError, ValueError) as ex:
        error_details = [ErrorDetail(description='Request body either either did not exist or was not valid JSON.')]
        raise FormValidationError(
            message='Form could not be validated due to given json not existing or being valid',
            error_details=error_details,
            schema=form_type.schema()
        ) from ex


def _build_error_details(errors) -> Sequence[FieldErrorDetail]:
    """
    Creates list of field error details from given pydantic errors

    :param errors: List of pydantic errors
    :return: List of field error details built from given pydantic errors
    """
    return [FieldErrorDetail(field_name='.'.join(error['loc']), description=error['msg']) for error in errors]
