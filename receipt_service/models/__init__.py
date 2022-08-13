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
