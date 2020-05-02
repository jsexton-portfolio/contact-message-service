from typing import Any, Union, Dict, Sequence, Optional

import jsonpickle
from chalice import Response

from chalicelib.helper import CamelCaseAttributesMixin


class ErrorDetail(CamelCaseAttributesMixin):
    """
    Represents any error information regarding a request. Will mostly be used in 400 Bad Request responses.
    """

    def __init__(self, field_name: str, description: str):
        self.field_name = field_name
        self.description = description


class MetaData(CamelCaseAttributesMixin):
    """
    Represents meta/introspected information about a response.
    """

    def __init__(self,
                 message: str,
                 error_details: Sequence[ErrorDetail] = None,
                 schemas: Dict[str, Any] = None):
        if schemas is None:
            schemas = {}
        if error_details is None:
            error_details = []

        self.message = message
        self.error_details = error_details
        self.schemas = schemas


class ResponseBody:
    """
    Represents a response originating from this API.

    All response bodies are expected to have success, meta and data fields.
    """

    def __init__(self, success: bool, meta: MetaData, data: Optional[Any] = None):
        self.success = success
        self.meta = meta
        self.data = data

    def to_json(self):
        return jsonpickle.dumps(self, unpicklable=False)


def ok_metadata() -> MetaData:
    """
    :return: Successful request (Ok) meta data
    """
    return MetaData(message='Request completed successfully')


def bad_metadata(error_details: Sequence[ErrorDetail], schema: Dict[str, Any]) -> MetaData:
    """
    :param error_details: Error details that will be used to construct meta data
    :param schema: Schema that will be used to construct meta data
    :return: Bad request meta data
    """
    return MetaData(
        message='Given inputs were incorrect. Consult the below details to address the issue.',
        error_details=error_details,
        schemas={'requestBody': schema})


def not_found_metadata(identifier: Union[str, int]) -> MetaData:
    """
    :param identifier: Identifier that will be used to construct message in meta data
    :return: Not found meta data
    """
    return MetaData(message=f'Resource with id {identifier} does not exist')


def internal_error_metadata() -> MetaData:
    """
    :return: Internal server error meta data
    """
    return MetaData(message='Request failed due to internal server error')


def ok(data: Any) -> Response:
    """
    :param data: Data that will be used to populate the response body
    :return: Ok response
    """
    return response(200, ok_metadata(), data)


def created(data: Any) -> Response:
    """
    :param data: Data that will be used to populate the response body
    :return: Created response
    """
    return response(201, meta=ok_metadata(), data=data)


def bad(error_details: Sequence[ErrorDetail], schema: Dict[str, Any] = None) -> Response:
    """
    :param error_details: Details detailing why the request was bad. These details will be used
    in the response body.
    :param schema: Request body  that will be displayed in meta information of response
    :return: Bad request response
    """
    if schema is None:
        schema = {}

    return response(400, bad_metadata(error_details, schema))


def not_found(identifier: Union[str, int]) -> Response:
    """
    :param identifier: Identifier that was used to attempt to select a resource, but could not.
    This value will be used in the body message description.
    :return: Not found response
    """
    return response(404, not_found_metadata(identifier))


def internal_error() -> Response:
    """
    :return: Internal server error response
    """
    return response(500, internal_error_metadata())


def response(status_code: int,
             meta: MetaData,
             data: Optional[Union[object, str]] = None,
             headers: Optional[dict] = None) -> Response:
    """
    Creates response instances from various information

    :param status_code: The status code that will be used to construct the response.
     Also used to determine if the response is a success or not. This information is populated in the body.
    :param meta: Response meta information
    :param data: Data element that will be used to populate the body content
    :param headers: Headers that will be used to construct the response
    :return: The created response information
    """
    success = status_code < 400
    body = ResponseBody(success=success, meta=meta, data=data)
    json_body = body.to_json()

    return Response(status_code=status_code, body=json_body, headers=headers)
