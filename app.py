from typing import Dict, Optional, Type

import pyocle
from chalice import Chalice, CognitoUserPoolAuthorizer
from mongoengine import connect
from pydantic.main import BaseModel

from chalicelib.form import ContactMessageCreationForm, ContactMessageQuery
from chalicelib.model import ContactMessageCollection
from chalicelib.service import ContactMessageService

app = Chalice(app_name='contact-message-service')

connection_string = pyocle.config.connection_string(default='')
connect(host=connection_string)

contact_message_service = ContactMessageService()
authorizer = CognitoUserPoolAuthorizer('portfolio-userpool',
                                       provider_arns=[
                                           'arn:aws:cognito-idp:us-east-2:811393626934:userpool/us-east-2_MLclIlI5Y'])


@app.route('/mail', methods=['POST'], cors=True)
@pyocle.error.error_handler
def create_contact_message():
    """
    Endpoint used for create contact messages. This endpoint is open to anonymous users.

    :return: The created response with created resource information
    """

    form = pyocle.form.resolve_form(app.current_request.raw_body, ContactMessageCreationForm)
    identity = app.current_request.context['identity']
    contact_message = contact_message_service.create_with_identity(form, identity)

    return pyocle.response.created(contact_message)


@app.route('/mail/{identifier}', methods=['GET'], cors=True, authorizer=authorizer)
@pyocle.error.error_handler
def get_single_contact_message(identifier: str):
    """
    Endpoint used to retrieve contact messages.

    :param identifier: The contact message id that will be used to find the specific contact message
    :return: The found contact message
    """

    contact_message = contact_message_service.find_one(identifier)
    return pyocle.response.ok(contact_message)


@app.route('/mail', methods=['GET'], cors=True, authorizer=authorizer)
@pyocle.error.error_handler
def get_multiple_contact_message():
    """
    Endpoint used to retrieve a specific contact message

    :return: The found contact messages
    """

    query = resolve_query(app.current_request.query_params, ContactMessageQuery)
    contact_messages = contact_message_service.find(**query)
    collection = ContactMessageCollection(contact_messages)
    return pyocle.response.ok(collection)


def resolve_query(params: Optional[Dict[str, str]], model: Type[BaseModel]):
    return {} if params is None else pyocle.form.resolve_form(params, model).dict(skip_defaults=True)
