from bson import ObjectId

from chalicelib.service import ContactMessageFormPublished


def contact_message_form_published_should_correctly_convert_id_to_string():
    form = ContactMessageFormPublished(
        contact_message_id=ObjectId(),
        sns_message_id='sns message id'
    )

    contact_message_id = form.contact_message_id
    assert isinstance(contact_message_id, str) is True
    assert ObjectId.is_valid(contact_message_id)
