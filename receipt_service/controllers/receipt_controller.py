from receipt_service.clients.ynab_client import YNABClient
from ..models import Transaction


class ReceiptController:
    budget_client = YNABClient()

    def get_transactions(self, transaction: Transaction) -> list[Transaction]:
        return self.budget_client.find_transactions(transaction)

    def get_transaction_id(self, transaction: Transaction) -> str:
        candidates = self._get_candidates(transaction, self.get_transactions(transaction))
        if candidates:
            return candidates[0].id

    @staticmethod
    def _get_candidates(transaction_to_find, transactions):
        res = []
        for t in transactions:
            if t.store_name == transaction_to_find.store_name and t.amount == transaction_to_find.amount:
                if t.date == transaction_to_find.date:
                    return [t]
                elif abs((t.date - transaction_to_find.date).days) < 2:
                    res.append(t)
        return res
