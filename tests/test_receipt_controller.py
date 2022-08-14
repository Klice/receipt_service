import datetime
from unittest.mock import Mock
import pytest
from receipt_service.controllers.receipt_controller import ReceiptController
from receipt_service.models import Transaction


@pytest.fixture
def receipt_controller():
    rc = ReceiptController()
    rc.budget_client = Mock()
    return rc


def test_receipt_controller_exists(receipt_controller: ReceiptController):
    assert receipt_controller


def test_receipt_controller_get_transactions(receipt_controller: ReceiptController):
    budget_client = receipt_controller.budget_client
    budget_client.find_transactions.return_value = ["1"]
    t = Transaction(None, store_name="1", date=datetime.date(2022, 1, 1), amount=1)
    assert receipt_controller.get_transactions(t) == ["1"]
    budget_client.find_transactions.assert_called_once_with(t)


@pytest.mark.parametrize("expected,transaction", [
    ("1", Transaction(None, "metro", datetime.date(2001, 1, 1), 1)),
    (None, Transaction(None, "metr2", datetime.date(2001, 1, 1), 1)),
    (None, Transaction(None, "metro", datetime.date(2001, 1, 1), 2)),
    ("1", Transaction(None, "metro", datetime.date(2001, 1, 2), 1)),
    ("1", Transaction(None, "metro", datetime.date(2000, 12, 31), 1)),
])
def test_get_correct_transanction(receipt_controller: ReceiptController, transaction, expected):
    t = Transaction("1", "metro", datetime.date(2001, 1, 1), 1)
    receipt_controller.budget_client.find_transactions.return_value = [t]
    assert receipt_controller.get_transaction_id(transaction) == expected
