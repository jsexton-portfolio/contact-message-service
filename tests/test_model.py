import pytest

from chalicelib.model import Reason


@pytest.mark.parametrize('reason', [
    'business',
    'BusINEss',
    'other',
    'OTHeR'
])
def test_reason_is_case_insensitive(reason):
    Reason(reason)
