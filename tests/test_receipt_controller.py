import datetime
from unittest.mock import Mock
import pytest
from receipt_service.controllers.receipt_controller import ReceiptController


@pytest.fixture
def receipt_controller():
    rc = ReceiptController()
    rc.budget_client = Mock()
    return rc


def test_receipt_controller_exists(receipt_controller: ReceiptController):
    assert receipt_controller


def test_receipt_controller_get_transactions(receipt_controller: ReceiptController):
    receipt_controller.budget_client.find_transactions.return_value = ["1"]
    assert receipt_controller.get_transactions(store_name="1", date=datetime.date(2022, 1, 1), amount=1) == ["1"]
