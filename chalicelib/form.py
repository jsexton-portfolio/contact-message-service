from typing import TypeVar, Type, Dict, Any, Optional, Sequence

from pydantic import BaseModel, Field, ValidationError, EmailStr, Extra

from chalicelib.model import Reason
from chalicelib.response import ErrorDetail


class FormValidationError(Exception):
    """
    Error raised when an incoming request form is invalid
    """

    def __init__(self,
                 error_details: Sequence[ErrorDetail],
                 message: str = None,
                 schema: Dict[str, Any] = None):
        if message is None:
            message = 'Form was not validated successfully'

        self.error_details = error_details
        self.message = message
        self.schema = schema
        super().__init__(message)


class SenderCreationForm(BaseModel):
    alias: str = Field(..., max_length=50)
    phone: Optional[str]
    email: EmailStr

    class Config:
        anystr_strip_whitespace = True
        extra = Extra.forbid


class ContactMessageCreationForm(BaseModel):
    message: str = Field(..., min_length=100, max_length=2000)
    reason: Reason
    sender: SenderCreationForm

    class Config:
        anystr_strip_whitespace = True
        extra = Extra.forbid


T = TypeVar('T')
SUPPORTED_FORM_TYPES = {
    ContactMessageCreationForm,
}


def resolve_form(json: Dict[str, Any], form_type: Type[T]) -> T:
    """
    Resolves a form from given type and json in the form of a dict. Validates form against given json
    and raises FormValidationError if form is invalid.

    :param json: The json that will be used to build the form
    :param form_type: The form type to resolve
    :return: The resolved form
    """
    if form_type not in SUPPORTED_FORM_TYPES:
        raise ValueError(f'Unsupported form type: {form_type.__name__}')

    try:
        return form_type(**json)
    except ValidationError as ex:
        error_details = _build_error_details(ex.errors())
        raise FormValidationError(error_details=error_details, schema=form_type.schema())


def _build_error_details(errors) -> Sequence[ErrorDetail]:
    """
    Creates list of error details from given pydantic errors

    :param errors: List of pydantic errors
    :return: List of error details built from given pydantic errors
    """
    return [ErrorDetail(field_name='.'.join(error['loc']), description=error['msg']) for error in errors]
