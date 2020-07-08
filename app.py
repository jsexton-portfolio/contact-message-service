from chalice import Chalice
from mongoengine import connect
import pyocle

from chalicelib.form import ContactMessageCreationForm
from chalicelib.service import ContactMessageService

app = Chalice(app_name='contact-message-service')

connection_string = pyocle.config.connection_string(default='')
connect(host=connection_string)

contact_message_service = ContactMessageService()


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
