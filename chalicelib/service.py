from typing import Dict, Any, Type, TypeVar, List, Union

import jsonpickle
from bson import ObjectId
from chalice.app import SNSEvent
from mongoengine import Document, DoesNotExist, QuerySet
from pyocle.serialization import CamelCaseAttributesMixin
from pyocle.service.core import ResourceNotFoundError
from pyocle.service.sns import SimpleNotificationService, PublishMessageForm

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
        return self._collect_to_list(self.document.objects(**kwargs))

    def find_paginated(self, page: int, limit: int, **kwargs) -> List[T]:
        offset = page * limit
        return self._collect_to_list(self.document.objects(**kwargs).skip(offset).limit(limit))

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

    def _collect_to_list(self, query_set: QuerySet) -> List[T]:
        return [document for document in query_set]


class ContactMessageFormPublished(CamelCaseAttributesMixin):
    """
    Class representing data field that will be presented in a response after publishing a
    create contact message form
    """

    def __init__(self,
                 contact_message_id: Union[str, ObjectId],
                 sns_message_id: str):
        if isinstance(contact_message_id, ObjectId):
            contact_message_id = str(contact_message_id)

        self.contact_message_id = contact_message_id
        self.sns_message_id = sns_message_id


class ContactMessageService(ResourceService):
    """
    Capable of interfacing with contact message resources
    """

    def __init__(self):
        super().__init__(ContactMessage)
        self.sns = SimpleNotificationService()

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

    def create_with_sns_event(self, event: SNSEvent) -> ContactMessage:
        """
        :param event:
        :return:
        """
        creation_form_dict = jsonpickle.decode(event.message)
        return super().create(creation_form_dict)

    def publish_form_with_identity(self,
                                   creation_form: ContactMessageCreationForm,
                                   identity: Dict[str, Any]) -> ContactMessageFormPublished:
        creation_form_dict = creation_form.dict()

        # We generate our contact message id now so that we can give this back for tracking purposes.
        # The message will not be inserted into the database until some time later
        identifier = ObjectId()
        creation_form_dict['id'] = str(identifier)
        creation_form_dict['sender']['ip'] = identity.get('sourceIp', 'unknown')
        creation_form_dict['sender']['user_agent'] = identity.get('userAgent', 'unknown')
        creation_form_dict['reason'] = creation_form_dict['reason'].value

        form = PublishMessageForm(
            message=creation_form_dict,
            topic_arn='arn:aws:sns:us-east-2:811393626934:contact-message-created',
        )
        response = self.sns.publish(form)

        return ContactMessageFormPublished(
            contact_message_id=identifier,
            sns_message_id=response['MessageId']
        )
