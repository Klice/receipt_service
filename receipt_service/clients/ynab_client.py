import datetime
from receipt_service.clients.api_client import APIClient
from receipt_service.models import Store


class YNABClient(APIClient):
    endpoints = [
        "/budgets/default/transactions"
    ]

    def find_transactions(self, store: Store, date: datetime.date, amount: int) -> list[str]:
        return self.get_budgets_default_transactions()
