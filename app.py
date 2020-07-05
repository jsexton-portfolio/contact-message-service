from chalice import Chalice
from mongoengine import connect
from pyocle import config
from pyocle.error import error_handler
from pyocle.form import resolve_form
from pyocle.response import created

from chalicelib.form import ContactMessageCreationForm
from chalicelib.service import ContactMessageService

app = Chalice(app_name='contact-message-service')

connection_string = config.connection_string()
connect(host=connection_string or '')

contact_message_service = ContactMessageService()


@app.route('/mail', methods=['POST'], cors=True)
@error_handler
def create_contact_message():
    """
    Endpoint used for create contact messages. This endpoint is open to anonymous users.

    :return: The created response with created resource information
    """
    form = resolve_form(app.current_request.raw_body, ContactMessageCreationForm)
    identity = app.current_request.context['identity']
    contact_message = contact_message_service.create_with_identity(form, identity)

    return created(contact_message)
