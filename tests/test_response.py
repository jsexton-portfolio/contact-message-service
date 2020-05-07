import pytest
from pydantic.main import BaseModel

from chalicelib.response import *


class DummyForm(BaseModel):
    first_name: str
    last_name: str


@pytest.fixture
def schema():
    return DummyForm.schema()


def test_ok_meta():
    meta = ok_metadata()
    assert meta.message == 'Request completed successfully'
    assert len(meta.error_details) == 0
    assert len(meta.schemas) == 0


def test_bad_message(schema):
    error_details = [
        ErrorDetail(description='description'),
        FieldErrorDetail(description='description', field_name='test_field')
    ]
    meta = bad_metadata(error_details=error_details, schema=schema)
    assert meta.message == 'Given inputs were incorrect. Consult the below details to address the issue.'
    assert len(meta.error_details) == 2
    assert 'requestBody' in meta.schemas.keys()


def test_not_found_message():
    identifier = '123'
    meta = not_found_metadata(identifier)
    assert meta.message == 'Resource with id 123 does not exist'
    assert len(meta.error_details) == 0


def test_internal_error_message():
    meta = internal_error_metadata()
    assert meta.message == 'Request failed due to internal server error'
    assert len(meta.error_details) == 0


def test_ok_response():
    data = {'field_name': 'field_value'}
    res = ok(data)

    body = jsonpickle.decode(res.body)

    assert res.status_code == 200
    assert body['success'] is True
    assert body['meta']['message'] == 'Request completed successfully'
    assert len(body['meta']['errorDetails']) == 0
    assert body['data'] == data
    assert res.headers == {}


def test_created_response():
    data = {'field_name': 'field_value'}
    res = created(data)

    body = jsonpickle.decode(res.body)

    assert res.status_code == 201
    assert body['success'] is True
    assert body['meta']['message'] == 'Request completed successfully'
    assert len(body['meta']['errorDetails']) == 0
    assert body['data'] == data
    assert res.headers == {}


def test_bad_response():
    error_details = [
        ErrorDetail(description='description'),
        FieldErrorDetail(description='description', field_name='test_field')
    ]
    res = bad(error_details)

    body = jsonpickle.decode(res.body)

    assert res.status_code == 400
    assert body['success'] is False
    assert body['meta'][
               'message'] == 'Given inputs were incorrect. Consult the below details to address the issue.'
    assert len(body['meta']['errorDetails']) == 2
    assert body['data'] is None
    assert res.headers == {}


def test_not_found_response():
    identifier = '123'
    res = not_found(identifier)

    body = jsonpickle.decode(res.body)

    assert res.status_code == 404
    assert body['success'] is False
    assert body['meta']['message'] == 'Resource with id 123 does not exist'
    assert len(body['meta']['errorDetails']) == 0
    assert body['data'] is None
    assert res.headers == {}


def test_internal_error_response():
    res = internal_error()

    body = jsonpickle.decode(res.body)

    assert res.status_code == 500
    assert body['success'] is False
    assert body['meta']['message'] == 'Request failed due to internal server error'
    assert len(body['meta']['errorDetails']) == 0
    assert body['data'] is None
    assert res.headers == {}
