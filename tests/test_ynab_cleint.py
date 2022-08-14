import datetime
import json
from unittest.mock import Mock
import pytest

from receipt_service.clients.ynab_client import YNABClient
from receipt_service.models import LineItems, Receipt, Store, Transaction


@pytest.fixture
def ynab_client():
    client = YNABClient()
    client.base_url = "http://test.com"
    client.network_client = Mock()
    return client


@pytest.fixture
def receipt():
    return Receipt(
        datetime.date(2000, 1, 1),
        [LineItems(1, 1, "l1"), LineItems(2, 2, "l2")],
        Store("", "", "", "Metro")
    )


@pytest.fixture
def ynab_transaction():
    return '''{
        "id": "id",
        "date": "2019-12-04",
        "amount": 1,
        "memo": "string",
        "cleared": "cleared",
        "approved": true,
        "flag_color": "red",
        "account_id": "string",
        "payee_id": "payee_id",
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
      }'''


@pytest.fixture
def transactions_response(ynab_transaction):
    return json.dumps(
        {"data": {
            "transactions": [json.loads(ynab_transaction)],
            "server_knowledge": 0
        }}
    )


@pytest.fixture
def transaction_response(ynab_transaction):
    return json.dumps(
        {"data": {
            "transaction": json.loads(ynab_transaction),
            "server_knowledge": 0
        }}
    )


def test_ynab_get_transactions(ynab_client: YNABClient, receipt, transactions_response):
    ynab_client.network_client.get.return_value = transactions_response
    res = ynab_client.find_transactions(receipt)
    params = {"since_date": "2000-01-01"}
    ynab_client.network_client.get.assert_called_once_with(
        "http://test.com/budgets/default/transactions",
        params=params,
        body=None
    )
    assert len(res) == 1
    assert isinstance(res[0], Transaction)
    assert res[0].id == "id"
    assert res[0].store_name == "payee_name"
    assert res[0].amount == 1
    assert res[0].date == datetime.date(2019, 12, 4)


def test_ynab_update_transaction(ynab_client: YNABClient, receipt, transaction_response):
    ynab_client.network_client.get.return_value = transaction_response
    ynab_client.network_client.put.return_value = '{}'
    ynab_client.update_transaction("1", receipt)
    subtransactions = ynab_client.network_client.put.call_args.kwargs['body']['subtransactions']
    assert len(subtransactions) == 2
    assert subtransactions[0]['amount'] == 1
    assert subtransactions[0]['payee_name'] == "payee_name"
    assert subtransactions[0]['payee_id'] == "payee_id"
    assert subtransactions[1]['amount'] == 2
