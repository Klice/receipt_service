import datetime
from unittest.mock import Mock
import pytest

from receipt_service.clients.ynab_client import YNABClient
from receipt_service.models import Transaction


@pytest.fixture
def ynab_client():
    client = YNABClient()
    client.network_client = Mock()
    return client


def test_ynab_parse_transactions(ynab_client: YNABClient):
    transaction = '''
{
  "data": {
    "transactions": [
      {
        "id": "id",
        "date": "2019-12-04",
        "amount": 1,
        "memo": "string",
        "cleared": "cleared",
        "approved": true,
        "flag_color": "red",
        "account_id": "string",
        "payee_id": "string",
        "category_id": "string",
        "transfer_account_id": "string",
        "transfer_transaction_id": "string",
        "matched_transaction_id": "string",
        "import_id": "string",
        "deleted": true,
        "account_name": "string",
        "payee_name": "payee_name",
        "category_name": "string",
        "subtransactions": [
          {
            "id": "string",
            "transaction_id": "string",
            "amount": 0,
            "memo": "string",
            "payee_id": "string",
            "payee_name": "string",
            "category_id": "string",
            "category_name": "string",
            "transfer_account_id": "string",
            "transfer_transaction_id": "string",
            "deleted": true
          }
        ]
      }
    ],
    "server_knowledge": 0
  }
}'''
    ynab_client.network_client.get.return_value = transaction
    res = ynab_client.find_transactions(store_name="1", date=datetime.date(2022, 1, 1))
    assert len(res) == 1
    assert isinstance(res[0], Transaction)
    assert res[0].id == "id"
    assert res[0].store_name == "payee_name"
    assert res[0].amount == 1
    assert res[0].date == datetime.date(2019, 12, 4)
