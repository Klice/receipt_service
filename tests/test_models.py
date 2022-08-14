import datetime
from receipt_service.models import Email, LineItems, Receipt, Store, Transaction


def test_models_store_init():
    store = Store(
        email="email@test.ca",
        id="metro",
        name="Metro1",
        budget_name="Metro2",
    )
    assert store.budget_name == "Metro2"
    assert store.name == "Metro1"
    assert store.id == "metro"
    assert store.email == "email@test.ca"


def test_models_store_defaulting_to_name():
    store = Store(
        email="email@test.ca",
        id="metro",
        name="Metro1",
    )
    assert store.budget_name == "Metro1"
    assert store.name == "Metro1"


def test_models_store_id_non_keyword():
    store = Store(
        "metro_id",
        email="email@test.ca",
        name="Metro1",
    )
    assert store.id == "metro_id"


def test_email_model_init():
    email = Email(
        store="store",
        date=datetime.date(2002, 12, 26),
        body="text",
    )

    assert email.store == "store"
    assert email.body == "text"


def test_transaction_model_init():
    transaction = Transaction(
        store_name="store",
        date=datetime.date(2002, 12, 26),
        id="text",
        amount=1
    )

    assert transaction.store_name == "store"
    assert transaction.amount == 1


def test_transaction_equal():
    assert Transaction("1", "2", datetime.date(2001, 1, 1), 1) == Transaction("1", "2", datetime.date(2001, 1, 1), 1)


def test_transaction_empty_id():
    assert Transaction(None, "2", datetime.date(2001, 1, 1), 1)


def test_transaction_from_dict_with_extra_keys():
    t = Transaction.from_dict({
        "amount": 1,
        "date": datetime.date(2000, 1, 1),
        "extra": "fff",
        "store_name": "store"
    })
    assert t == Transaction(None, "store", datetime.date(2000, 1, 1), 1)


def test_receipt():
    assert Receipt(
        date=datetime.date(2000, 1, 1),
        store=Store("store", "store", "email", "store"),
        line_items=[
            LineItems(amount=1, name="l1", quantity=1)
        ]
    )


def test_receipt_total_amount():
    r = Receipt(
        date=datetime.date(2000, 1, 1),
        store=Store("id", "name", "email", "budget_name"),
        line_items=[
            LineItems(amount=1, name="l1", quantity=1),
            LineItems(amount=3, name="l1", quantity=1),
            LineItems(amount=5, name="l1", quantity=1),
        ]
    )
    assert r.amount == 9


def test_receipt_to_transaction():
    t = Receipt(
        date=datetime.date(2000, 1, 1),
        store=Store("id", "name", "email", "budget_name"),
        line_items=[
            LineItems(amount=1, name="l1", quantity=1),
            LineItems(amount=3, name="l1", quantity=1),
            LineItems(amount=5, name="l1", quantity=1),
        ]
    ).to_transaction()
    assert t == Transaction(None, "budget_name", datetime.date(2000, 1, 1), 9)
