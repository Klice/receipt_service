from receipt_service.clients.ynab_client import YNABClient
from ..models import Receipt


class ReceiptController:
    budget_client = YNABClient()

    def get_transaction_id(self, receipt: Receipt) -> str:
        transaction = receipt.to_transaction()
        candidates = self._get_candidates(transaction, self.budget_client.find_transactions(transaction))
        if candidates:
            return candidates[0].id

    def update_transaction(self, transaction, receipt):
        self.budget_client.update_transaction(transaction, receipt)

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
