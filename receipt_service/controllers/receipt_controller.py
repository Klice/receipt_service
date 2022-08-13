from receipt_service.clients.ynab_client import YNABClient


class ReceiptController:
    budget_client = YNABClient()

    def get_transactions(self, store_name, date, amount):
        return self.budget_client.find_transactions()
