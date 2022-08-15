import datetime
import pytest
from receipt_service.clients.ynab_client import YNABClient
from receipt_service.models import LineItems, Receipt, Store


@pytest.fixture
def client():
    return YNABClient()


@pytest.fixture
def receipt():
    return Receipt(
        date=datetime.date(2017, 10, 8),
        line_items=[
            LineItems(-35140, 1, 1),
            LineItems(-20000, 1, 1),
        ],
        store=Store("1", "Metro", "", "Metro")
    )


@pytest.mark.integtest
def test_get_payee_by_name(client: YNABClient):
    assert client.get_payee_by_name("Metro") == "3e366c76-dc8a-47f7-8492-c7d9a6cd15b5"


@pytest.mark.integtest
def test_find_transaction(client: YNABClient, receipt):
    transactions = client.find_transactions(receipt)
    transactions.sort(key=lambda x: x.date, reverse=True)
    assert transactions[-1].id == '8388c777-64de-4036-b8c4-378639a3910b'


@pytest.mark.skip(reason="no delete functionality")
@pytest.mark.integtest
def test_update_transaction_empty_subtransactions(client: YNABClient, receipt: Receipt):
    receipt.line_items = []
    transaction = client.get_transaction('8388c777-64de-4036-b8c4-378639a3910b')
    for t in transaction["subtransactions"]:
        client.delete_transaction(t["transaction_id"])
    # client.update_transaction('8388c777-64de-4036-b8c4-378639a3910b', receipt)
    transaction = client.get_transaction('8388c777-64de-4036-b8c4-378639a3910b')
    assert len(transaction["subtransactions"]) == 0


@pytest.mark.skip(reason="no delete functionality, can't clean up after inserting")
@pytest.mark.integtest
def test_update_transaction(client: YNABClient, receipt):
    client.update_transaction('8388c777-64de-4036-b8c4-378639a3910b', receipt)
    transaction = client.get_transaction('8388c777-64de-4036-b8c4-378639a3910b')
    assert len(transaction["subtransactions"]) == 2
