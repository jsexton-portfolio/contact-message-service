import pytest
from chalice.test import Client
from pyocle.form import FormValidationError
from pyocle.service.core import ResourceNotFoundError

import app
from chalicelib.service import ContactMessageService


@pytest.fixture
def client():
    with Client(app.app) as test_client:
        yield test_client


def test_create_contact_message_responds_correctly(mocker, client,
                                                   ok_json,
                                                   message_form_published_json,
                                                   message_form_published):
    mocker.patch('pyocle.form.resolve_form', return_value={})
    mocker.patch.object(ContactMessageService, 'publish_form_with_identity', return_value=message_form_published)
    actual_response = client.http.request('POST', '/mail')

    assert actual_response.status_code == 202
    assert actual_response.json_body == ok_json(message_form_published_json)


def test_create_contact_message_handles_bad_request(mocker, client, bad_request_json):
    mocker.patch('pyocle.form.resolve_form', side_effect=FormValidationError())
    actual_response = client.http.request('POST', '/mail')

    assert actual_response.status_code == 400
    assert actual_response.json_body == bad_request_json()


def test_create_contact_message_handles_internal_server_error(mocker, client, server_error_json):
    mocker.patch('pyocle.form.resolve_form', return_value={})
    mocker.patch.object(ContactMessageService, 'publish_form_with_identity', side_effect=Exception())
    actual_response = client.http.request('POST', '/mail')

    assert actual_response.status_code == 500
    assert actual_response.json_body == server_error_json


def test_get_message_responds_correctly(mocker, client, contact_message, contact_message_json, ok_json):
    mocker.patch.object(ContactMessageService, 'find_one', return_value=contact_message)
    actual_response = client.http.request('GET', '/mail/123')

    assert actual_response.status_code == 200
    assert actual_response.json_body == ok_json(contact_message_json)


def test_get_message_correctly_handles_not_found(mocker, client, not_found_json):
    mocker.patch.object(ContactMessageService, 'find_one', side_effect=ResourceNotFoundError('123'))
    actual_response = client.http.request('GET', '/mail/123')

    assert actual_response.status_code == 404
    assert actual_response.json_body == not_found_json('123')


def test_get_message_correctly_handles_internal_server_error(mocker, client, server_error_json):
    mocker.patch.object(ContactMessageService, 'find_one', side_effect=Exception())
    actual_response = client.http.request('GET', '/mail/123')

    assert actual_response.status_code == 500
    assert actual_response.json_body == server_error_json
