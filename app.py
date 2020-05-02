import os

from chalice import Chalice
from mongoengine import connect

from chalicelib.error import error_handler
from chalicelib.form import resolve_form, ContactMessageCreationForm
from chalicelib.response import created
from chalicelib.service import ContactMessageService

app = Chalice(app_name='contact-message-service')

connection_string = os.getenv('CONNECTION_STRING')
connect(connection_string)

contact_message_service = ContactMessageService()


@app.route('/mail', methods=['POST'])
@error_handler
def create_contact_message():
    """
    Endpoint used for create contact messages. This endpoint is open to anonymous users.

    :return: The created response with created resource information
    """
    form = resolve_form(app.current_request.json_body, ContactMessageCreationForm)
    identity = app.current_request.context['identity']
    contact_message = contact_message_service.create_with_identity(form, identity)

    return created(contact_message)
