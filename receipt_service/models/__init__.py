from dataclasses import dataclass
import datetime


@dataclass
class Store:
    id: str
    name: str
    email: str
    budget_name: str = None

    def __post_init__(self):
        if self.budget_name is None:
            self.budget_name = self.name


@dataclass
class Email:
    store: Store
    date: datetime.date
    body: str


@dataclass
class Transaction:
    id: str
    store_name: str
    date: datetime.date
    amount: int

    @staticmethod
    def from_dict(data):
        return Transaction(
            id=data.get("id"),
            store_name=data.get("store_name"),
            date=data.get("date"),
            amount=data.get("amount"),
        )


@dataclass
class LineItems:
    amount: int
    quantity: int
    name: str


@dataclass
class Receipt:
    date: datetime.date
    line_items: list[LineItems]

    @property
    def amount(self):
        return sum([line_item.amount for line_item in self.line_items])
