from datetime import date
from receipt_service.clients.api_client import APIClient
from receipt_service.models import Transaction


class YNABClient(APIClient):
    endpoints = [
        "/budgets/default/transactions"
    ]

    def find_transactions(self, store_name: str, date: date) -> list[Transaction]:
        res = []
        for t in self.get_budgets_default_transactions()["data"]["transactions"]:
            res.append(Transaction(
                id=t["id"],
                store_name=t["payee_name"],
                date=date.fromisoformat(t["date"]),
                amount=t["amount"]
            ))
        return res
