from typing import Dict, Any, Type, TypeVar, List

from bson import ObjectId
from mongoengine import Document, DoesNotExist
from pyocle.error import ResourceNotFoundError

from chalicelib.form import ContactMessageCreationForm
from chalicelib.model import ContactMessage

T = TypeVar('T', bound=Document)


class ResourceService:
    """
    General resource provider capable of basic and common resource selection and manipulation
    """

    def __init__(self, document: Type[T]):
        self.document = document

    def create(self, creation_form: Dict[str, Any]) -> T:
        return self.document(**creation_form).save()

    def find(self, **kwargs) -> List[T]:
        return [document for document in self.document.objects(**kwargs)]

    def find_one(self, identifier: str) -> T:
        """
        Selects a single resource with given identifier. Raises ResourceNotFoundError if no resource existed
        with the given identifier.

        :param identifier: The identifier that will be used to select the specific resource
        :return: The selected resource
        """
        if not ObjectId.is_valid(identifier):
            raise ResourceNotFoundError(identifier)

        try:
            return self.document.objects.get(id=identifier)
        except DoesNotExist:
            raise ResourceNotFoundError(identifier)


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
