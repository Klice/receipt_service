from receipt_service.models import Store
from receipt_service.controllers.store_controller import StoreController


def test_store_controller_saves_store():
    store = Store("id", "name", "email")
    sc = StoreController().add(store).add(store)
    assert len(sc.get_stores()) == 2
