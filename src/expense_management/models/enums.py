from __future__ import annotations

from enum import Enum


def enum_values(enum_cls: type[Enum]) -> list[str]:
    return [item.value for item in enum_cls]


class AccountType(str, Enum):
    CASH = "cash"
    BANK = "bank"
    CREDIT_CARD = "credit_card"
    WALLET = "wallet"
    INVESTMENT = "investment"
    LOAN = "loan"


class AccountStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    CLEARED = "cleared"
    VOID = "void"


class BudgetPeriod(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class RecurringFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class AttachmentType(str, Enum):
    RECEIPT = "receipt"
    INVOICE = "invoice"
    NOTE = "note"
    OTHER = "other"
