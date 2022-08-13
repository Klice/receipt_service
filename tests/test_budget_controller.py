from receipt_service.controllers.budget_controller import BudgetController


def test_budget_controller():
    bc = BudgetController()
    assert bc
