import datetime
import json
from unittest.mock import ANY, Mock
import pytest

from receipt_service.clients.ynab_client import YNABClient, YNABError
from receipt_service.models import LineItems, Receipt, Store, Transaction


@pytest.fixture
def ynab_client():
    client = YNABClient()
    client.base_url = "http://test.com"
    client.network_client = Mock()
    client.auth = None
    client.request_processor = None
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
def ynab_transaction_parent():
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
        "parent_transaction_id": "string"
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
def transactions_response_with_parent(ynab_transaction_parent):
    return json.dumps(
        {"data": {
            "transactions": [json.loads(ynab_transaction_parent)],
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


def test_ynab_get_transactions_subtrans(ynab_client: YNABClient, receipt, transactions_response_with_parent):
    ynab_client.get_payee_by_name = lambda x: "payees123"
    ynab_client.network_client.get.return_value = transactions_response_with_parent
    res = ynab_client.find_transactions(receipt)
    params = {"since_date": "2000-01-01"}
    ynab_client.network_client.get.assert_called_once_with(
        url=f"http://test.com/budgets/{ynab_client.budget}/payees/payees123/transactions",
        params=params,
        data=None,
        headers=ynab_client.headers,
    )
    assert len(res) == 0


def test_ynab_get_transactions(ynab_client: YNABClient, receipt, transactions_response):
    ynab_client.get_payee_by_name = lambda x: "payees123"
    ynab_client.network_client.get.return_value = transactions_response
    res = ynab_client.find_transactions(receipt)
    params = {"since_date": "2000-01-01"}
    ynab_client.network_client.get.assert_called_once_with(
        url=f"http://test.com/budgets/{ynab_client.budget}/payees/payees123/transactions",
        params=params,
        data=None,
        headers=ynab_client.headers,
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
    subtransactions = ynab_client.network_client.put.call_args.kwargs['data']['transaction']['subtransactions']
    assert len(subtransactions) == 2
    assert subtransactions[0]['amount'] == 1
    assert subtransactions[0]['payee_name'] == "payee_name"
    assert subtransactions[0]['payee_id'] == "payee_id"
    assert subtransactions[1]['amount'] == 2


def test_delete_transaction(ynab_client: YNABClient):
    ynab_client.network_client.delete.return_value = '{}'
    ynab_client.delete_transaction("1")
    ynab_client.network_client.delete.assert_called_once_with(
        url=f"http://test.com/budgets/{ynab_client.budget}/transactions/1",
        params=ANY,
        data=ANY,
        headers=ANY,
    )


def test_get_payee_id_by_name(ynab_client: YNABClient):
    payee_response = '''{
  "data": {
    "payees": [
      {
        "id": "id",
        "name": "name",
        "transfer_account_id": "string",
        "deleted": true
      },
      {
        "id": "metro_id",
        "name": "metro",
        "transfer_account_id": "string",
        "deleted": true
      },
      {
        "id": "metro_id2",
        "name": "metro",
        "transfer_account_id": "string",
        "deleted": false
      }
    ],
    "server_knowledge": 0
  }
}'''
    ynab_client.network_client.get.return_value = payee_response
    payee_id = ynab_client.get_payee_by_name("metro")
    called_url = ynab_client.network_client.get.call_args.kwargs["url"]
    assert called_url == f"http://test.com/budgets/{ynab_client.budget}/payees"
    assert payee_id == "metro_id2"


def test_error_should_rise_exception(ynab_client: YNABClient):
    ynab_client.network_client.get.return_value = '''{
  "error": {
    "id": "123",
    "name": "error_name",
    "detail": "Error detail"
  }
}'''
    with pytest.raises(YNABError) as exc_info:
        ynab_client.get_payee_by_name("metro")

    assert exc_info.value.id == "123"
    assert exc_info.value.name == "error_name"
    assert exc_info.value.detail == "Error detail"
