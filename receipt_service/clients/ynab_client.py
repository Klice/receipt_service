from dataclasses import dataclass
from datetime import date
import json
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

    def response_processor(self, x):
        res = json.loads(x)
        if "error" in res:
            raise YNABError(**res["error"])
        return res

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
        ret = self._filter_subtransactions(ret)
        return self._response_to_transactions(ret)

    def _filter_subtransactions(self, ret):
        transactions = ret["data"]["transactions"]
        ret["data"]["transactions"] = [t for t in transactions if not self._is_subtransaction(t)]
        return ret

    @staticmethod
    def _is_subtransaction(transactions):
        return "parent_transaction_id" in transactions and transactions["parent_transaction_id"]

    def update_transaction(self, transaction_id, receipt):
        transaction = self.get_transaction(transaction_id)
        request = {
            "transaction": {
                "account_id": transaction["account_id"],
                "amount": transaction["amount"],
                "subtransactions": self._get_subtransactions(
                    receipt,
                    transaction["payee_id"],
                    transaction["payee_name"],
                    transaction["category_id"],
                )
            }
        }
        self.put_budgets_budget_id_transactions_transaction_id(
            transaction_id=transaction_id,
            budget_id=self.budget,
            data=request
        )

    def get_transaction(self, transaction_id):
        return self.get_budgets_budget_id_transactions_transaction_id(
            transaction_id=transaction_id,
            budget_id=self.budget
        )["data"]["transaction"]

    def delete_transaction(self, transaction_id):
        self.delete_budgets_budget_id_transactions_transaction_id(
            transaction_id=transaction_id,
            budget_id=self.budget,
        )

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


@dataclass
class YNABError(Exception):
    id: str
    name: str
    detail: str

    def __str__(self):
        return f'Error: {self.id} [{self.name}]: {self.detail}'
