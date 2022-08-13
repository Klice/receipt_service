from ..models import Store


class StoreController:
    _stores = None

    def __init__(self):
        self._stores = []

    def add(self, store: Store):
        self._stores.append(store)
        return self

    def get_stores(self) -> list[Store]:
        return self._stores
