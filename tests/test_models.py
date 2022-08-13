import datetime
from receipt_service.models import Email, Store


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
