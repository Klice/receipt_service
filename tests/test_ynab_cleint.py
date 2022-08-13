import datetime
from unittest.mock import Mock
import pytest

from receipt_service.clients.ynab_client import YNABClient


@pytest.fixture
def ynab_client():
    client = YNABClient()
    client.network_client = Mock()
    return client


def test_ynab_find_transactions(ynab_client: YNABClient):
    ynab_client.network_client.get.return_value = '["1"]'
    res = ynab_client.find_transactions(store="1", date=datetime.date(2022, 1, 1), amount=1)

    ynab_client.network_client.get.assert_called_once()
    assert res == ["1"]
