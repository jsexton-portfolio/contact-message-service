import pytest


@pytest.fixture
def get_fixture(request):
    def _get_fixture_by_name(name):
        return request.getfixturevalue(name)

    return _get_fixture_by_name
