from typing import Type, TypeVar, Generic, Dict, Any

from mongoengine import Document

from chalicelib.form import ContactMessageCreationForm
from chalicelib.model import ContactMessage


class ResourceNotFoundError(Exception):
    """
    Error raised when a resource could not be found with a particular identifier.
    """

    def __init__(self, identifier: str, message: str = None):
        if message is None:
            message = f'Resource with id {identifier} could not be found'

        self.identifier = identifier
        self.message = message
        super().__init__(self.message)


# Type representing the document the resource service interfaces with
T = TypeVar('T', bound=Document)


class ResourceService(Generic[T]):
    """
    Service containing common resource manipulation and retrieval functionality.
    """

    def __init__(self, document: Type[T]):
        self.document = document

    def create(self, form: Dict[str, Any]) -> T:
        """

        :param form:
        :return:
        """
        return self.document(**form).save()


class ContactMessageService(ResourceService):
    def __init__(self):
        super().__init__(ContactMessage)

    def create_with_identity(self,
                             creation_form: ContactMessageCreationForm,
                             identity: Dict[str, Any]) -> ContactMessage:
        creation_form_dict = creation_form.dict()

        # Fuckin hate this. Make create an object and map this identity dictionary to it?
        creation_form_dict['sender']['ip'] = identity.get('sourceIp', 'unknown')
        creation_form_dict['sender']['user_agent'] = identity.get('userAgent', 'unknown')

        # Should create custom mongo engine field for enums in the future that do this conversion for us
        creation_form_dict['reason'] = creation_form_dict['reason'].value

        return self.document(**creation_form_dict).save()
