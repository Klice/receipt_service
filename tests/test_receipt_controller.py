import datetime
from unittest.mock import Mock
import pytest
from receipt_service.controllers.receipt_controller import ReceiptController
from receipt_service.models import LineItems, Receipt, Store, Transaction


@pytest.fixture
def receipt_controller():
    rc = ReceiptController()
    rc.budget_client = Mock()
    return rc


@pytest.fixture
def budget_response():
    return Transaction("1", "metro", datetime.date(2001, 1, 1), 1)


@pytest.fixture
def budget_client(receipt_controller, budget_response):
    receipt_controller.budget_client.find_transactions.return_value = [budget_response]
    return receipt_controller.budget_client


def test_receipt_controller_exists(receipt_controller: ReceiptController):
    assert receipt_controller


def test_receipt_controller_get_transactions_calls_budget(receipt_controller, budget_client, budget_response):
    r = Receipt(budget_response.date, [LineItems(1, 1, "l")], Store("id", "name", "email", budget_response.store_name))
    assert receipt_controller.get_transaction_id(r) == "1"
    budget_client.find_transactions.assert_called_once_with(r.to_transaction())


@pytest.mark.parametrize("expected,receipt", [
    ("1", Receipt(datetime.date(2001, 1, 1), [LineItems(1, 1, "")], Store("", "", "", "metro"))),
    (None, Receipt(datetime.date(2001, 1, 1), [LineItems(1, 1, "")], Store("", "", "", "metro2"))),
    (None, Receipt(datetime.date(2001, 1, 1), [LineItems(2, 1, "")], Store("", "", "", "metro"))),
    ("1", Receipt(datetime.date(2001, 1, 2), [LineItems(1, 1, "")], Store("", "", "", "metro"))),
    ("1", Receipt(datetime.date(2000, 12, 31), [LineItems(1, 1, "")], Store("", "", "", "metro"))),
    (None, Receipt(datetime.date(2000, 1, 2), [LineItems(1, 1, "")], Store("", "", "", "metro"))),
])
def test_get_correct_transanction(receipt_controller, receipt, expected, budget_client):
    assert receipt_controller.get_transaction_id(receipt) == expected
    assert budget_client.find_transactions.call_count == 1


def test_update_transaction(receipt_controller, budget_client):
    r = Receipt(datetime.date(2000, 1, 2), [LineItems(1, 1, "")], Store("", "", "", "metro"))
    t = Transaction("1", "metro", datetime.date(2001, 1, 1), 1)
    receipt_controller.update_transaction(t, r)
    budget_client.update_transaction.assert_called_once_with(t, r)
