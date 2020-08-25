import pyocle
from chalice import Chalice, CognitoUserPoolAuthorizer
from chalice.app import SNSEvent
from mongoengine import connect
from pyocle.service.ses import TemplatedEmailForm, SimpleEmailService

from chalicelib.form import ContactMessageCreationForm, ContactMessageQueryParameters
from chalicelib.model import ContactMessageCollection
from chalicelib.service import ContactMessageService

app = Chalice(app_name='contact-message-service')
app.log.setLevel('DEBUG')

connection_string = pyocle.config.connection_string(default='')
connect(host=connection_string)

cms = ContactMessageService()
authorizer = CognitoUserPoolAuthorizer('portfolio-userpool',
                                       provider_arns=[
                                           'arn:aws:cognito-idp:us-east-2:811393626934:userpool/us-east-2_MLclIlI5Y'])


@app.route('/mail', methods=['POST'], cors=True)
@pyocle.response.error_handler
def create_contact_message():
    """
    Endpoint used for create contact messages. This endpoint is open to anonymous users.

    :return: The created response with created resource information
    """

    form = pyocle.form.resolve_form(app.current_request.raw_body, ContactMessageCreationForm)
    identity = app.current_request.context['identity']
    published_form = cms.publish_form_with_identity(form, identity)
    return pyocle.response.accepted(published_form)


@app.route('/mail/{identifier}', methods=['GET'], cors=True, authorizer=authorizer)
@pyocle.response.error_handler
def get_single_contact_message(identifier: str):
    """
    Endpoint used to retrieve contact messages.

    :param identifier: The contact message id that will be used to find the specific contact message
    :return: The found contact message
    """

    contact_message = cms.find_one(identifier)
    return pyocle.response.ok(contact_message)


@app.route('/mail', methods=['GET'], cors=True, authorizer=authorizer)
@pyocle.response.error_handler
def get_multiple_contact_message():
    """
    Endpoint used to retrieve a specific contact message

    :return: The found contact messages
    """

    query_params = pyocle.form.resolve_query_params(app.current_request.query_params, ContactMessageQueryParameters)
    contact_messages = cms.find_paginated(**query_params.dict(exclude_none=True))
    collection = ContactMessageCollection(contact_messages)
    return pyocle.response.ok(collection, query_params)


@app.on_sns_message('contact-message-created')
def send_email_on_received(event: SNSEvent):
    """
    :param event:
    :return:
    """
    form = TemplatedEmailForm(
        source='JS Portfolio <no-reply@justinsexton.net>',
        to_addresses=[
            'justinsexton.dev@gmail.com'
        ],
        configuration_set='contact-message-created',
        template='contact-message-created',
        template_data=event.message
    )
    response = SimpleEmailService().send_templated_email(form)
    app.log.info(f'Contact message created notification email sent.')
    app.log.debug(response)


@app.on_sns_message('contact-message-created')
def insert_into_database_on_received(event: SNSEvent):
    """
    :param event:
    :return:
    """
    contact_message = cms.create_with_sns_event(event)
    app.log.info(f'Contact message created: {contact_message}')
