from typing import Dict, Any, Type, TypeVar

from mongoengine import Document

from chalicelib.form import ContactMessageCreationForm
from chalicelib.model import ContactMessage

T = TypeVar('T', bound=Document)


class ResourceService:
    """
    General resource provider capable of basic and common resource selection and manipulation
    """

    def __init__(self, document: Type[T]):
        self.document = document

    def create(self, creation_form: Dict[str, Any]):
        return self.document(**creation_form).save()


class ContactMessageService(ResourceService):
    """
    Capable of interfacing with contact message resources
    """

    def __init__(self):
        super().__init__(ContactMessage)

    def create_with_identity(self,
                             creation_form: ContactMessageCreationForm,
                             identity: Dict[str, Any]) -> ContactMessage:
        creation_form_dict = creation_form.dict()

        # Hate this. Make create an object and map this identity dictionary to it?
        creation_form_dict['sender']['ip'] = identity.get('sourceIp', 'unknown')
        creation_form_dict['sender']['user_agent'] = identity.get('userAgent', 'unknown')

        # Should create custom mongo engine field for enums in the future that do this conversion
        # is completed more naturally
        creation_form_dict['reason'] = creation_form_dict['reason'].value

        return super().create(creation_form_dict)
