from datetime import date
from receipt_service.clients.api_client import APIClient, BearerAuth
from receipt_service.models import Receipt, Transaction
from receipt_service.utils.config import get_conf


class YNABClient(APIClient):
    auth = BearerAuth(token=get_conf("YNAB_TOKEN"))
    base_url = "https://api.youneedabudget.com/v1"
    endpoints = [
        "budgets/{budget_id}/transactions",
        "budgets/{budget_id}/transactions/{transaction_id}",
        "budgets/{budget_id}/payees/{payee_id}/transactions",
        "budgets/{budget_id}/payees",
    ]
    budget = get_conf("YNAB_BUDGET")

    def get_payee_by_name(self, name):
        payees = self.get_budgets_budget_id_payees(budget_id=self.budget)["data"]["payees"]
        for p in payees:
            if p["name"] == name and not p["deleted"]:
                return p["id"]

    def find_transactions(self, receipt: Receipt) -> list[Transaction]:
        payee_id = self.get_payee_by_name(receipt.store.budget_name)
        ret = self.get_budgets_budget_id_payees_payee_id_transactions(
            params={"since_date": str(receipt.date)},
            budget_id=self.budget,
            payee_id=payee_id
        )
        return self._response_to_transactions(ret)

    def update_transaction(self, transaction_id, receipt):
        transaction = self.get_transaction(transaction_id)
        transaction["subtransactions"] = self._get_subtransactions(
            receipt,
            transaction["payee_id"],
            transaction["payee_name"],
            transaction["category_id"],
        )
        self.put_budgets_budget_id_transactions_transaction_id(
            transaction_id=transaction_id,
            budget_id=self.budget,
            data=transaction
        )

    def get_transaction(self, transaction_id):
        return self.get_budgets_budget_id_transactions_transaction_id(
            transaction_id=transaction_id,
            budget_id=self.budget
        )["data"]["transaction"]

    @staticmethod
    def _get_subtransactions(receipt: Receipt, payee_id, payee_name, category_id):
        res = []
        for li in receipt.line_items:
            res.append(
                {
                    "amount": li.amount,
                    "payee_id": payee_id,
                    "payee_name": payee_name,
                    "category_id": category_id,
                }
            )
        return res

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
