from datetime import date
from receipt_service.clients.api_client import APIClient
from receipt_service.models import Transaction


class YNABClient(APIClient):
    endpoints = [
        "budgets/default/transactions"
    ]

    def find_transactions(self, transaction) -> list[Transaction]:
        ret = self.get_budgets_default_transactions(params={"since_date": str(transaction.date)})
        return self._response_to_transactions(ret)

    @staticmethod
    def _response_to_transactions(response):
        res = []
        for t in response["data"]["transactions"]:
            res.append(Transaction(
                id=t["id"],
                store_name=t["payee_name"],
                date=date.fromisoformat(t["date"]),
                amount=t["amount"]
            ))
        return res
