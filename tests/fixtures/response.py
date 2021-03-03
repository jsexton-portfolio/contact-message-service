from typing import Dict, Any

import pytest


@pytest.fixture
def ok_json():
    def ok(data: Dict[str, Any]):
        return {
            "success": True,
            "meta": {
                "message": 'Request completed successfully',
                "errorDetails": [],
                "paginationDetails": {},
                "schemas": {}
            },
            "data": data
        }

    return ok


@pytest.fixture
def bad_request_json():
    def bad_request():
        return {
            "success": False,
            "meta": {
                "message": 'Given inputs were incorrect. Consult the below details to address the issue.',
                "errorDetails": [],
                "paginationDetails": {},
                "schemas": {}
            },
            "data": None
        }

    return bad_request


@pytest.fixture
def not_found_json():
    def not_found(identifier: id) -> Dict[str, Any]:
        return {
            "success": False,
            "meta": {
                "message": f'Resource with id {identifier} does not exist',
                "errorDetails": [],
                "paginationDetails": {},
                "schemas": {}
            },
            "data": None
        }

    return not_found


@pytest.fixture
def server_error_json():
    return {
        "success": False,
        "meta": {
            "message": "Request failed due to internal server error",
            "errorDetails": [],
            "paginationDetails": {},
            "schemas": {}
        },
        "data": None
    }
