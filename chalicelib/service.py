import base64
from typing import Dict, Any, Type, TypeVar

import boto3
from mongoengine import Document

from chalicelib.form import ContactMessageCreationForm
from chalicelib.model import ContactMessage


class ServiceError(Exception):
    """
    Any error that may be raised from a service
    """
    pass


class ResourceNotFoundError(ServiceError):
    """
    Error raised when a resource could not be found with a particular identifier.
    """

    def __init__(self, identifier: str, message: str = None):
        self.identifier = identifier
        self.message = message or f'Resource with id {identifier} could not be found'


T = TypeVar('T', bound=Document)


class ResourceService:
    def __init__(self, document: Type[T]):
        self.document = document

    def create(self, creation_form: Dict[str, Any]):
        return self.document(**creation_form).save()


class ContactMessageService(ResourceService):
    def __init__(self):
        super().__init__(ContactMessage)

    def create_with_identity(self,
                             creation_form: ContactMessageCreationForm,
                             identity: Dict[str, Any]) -> ContactMessage:
        creation_form_dict = creation_form.dict()

        # Hate this. Make create an object and map this identity dictionary to it?
        creation_form_dict['sender']['ip'] = identity.get('sourceIp', 'unknown')
        creation_form_dict['sender']['user_agent'] = identity.get('userAgent', 'unknown')

        # Should create custom mongo engine field for enums in the future that do this conversion for us
        creation_form_dict['reason'] = creation_form_dict['reason'].value

        # return self.document(**creation_form_dict).save()
        return super().create(creation_form_dict)


class KeyManagementService:
    """
    Service used to interface with aws kms (Key Management Service)

    WARNING: Currently does not gracefully handle when a key identifier is unauthorized for use.
    """

    def __init__(self):
        self.client = boto3.client('kms')

    def encrypt(self, plaintext: str, key_id: str) -> Dict[str, Any]:
        """
        Encrypts given plaintext with specified key identifier.

        :param plaintext: The plaintext to encrypt
        :param key_id: The key identifier to use when encrypting the given plaintext
        :return: The kms encryption response
        """

        encryption_response = self.client.encrypt(KeyId=key_id, Plaintext=plaintext)
        return encryption_response

    def decrypt(self, ciphertext: str) -> Dict[str, Any]:
        """
        Decrypts given ciphertext

        :param ciphertext: The ciphertext to decrypt
        :return: The kms decrypting response
        """

        base64_decoded_connection_string_cipher_text = base64.b64decode(ciphertext)
        decryption_response = self.client.decrypt(CiphertextBlob=base64_decoded_connection_string_cipher_text)
        return decryption_response
