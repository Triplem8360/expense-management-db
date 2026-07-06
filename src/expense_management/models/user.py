from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from expense_management.db.base import Base
from expense_management.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from expense_management.models.account import Account
    from expense_management.models.budget import Budget
    from expense_management.models.category import Category
    from expense_management.models.merchant import Merchant
    from expense_management.models.recurring_transaction import RecurringTransaction
    from expense_management.models.tag import Tag
    from expense_management.models.transaction import Transaction


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(150), default=None)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    default_currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    accounts: Mapped[list[Account]] = relationship(
        "Account",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    categories: Mapped[list[Category]] = relationship(
        "Category",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    merchants: Mapped[list[Merchant]] = relationship(
        "Merchant",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    transactions: Mapped[list[Transaction]] = relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    budgets: Mapped[list[Budget]] = relationship(
        "Budget",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    tags: Mapped[list[Tag]] = relationship(
        "Tag",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    recurring_transactions: Mapped[list[RecurringTransaction]] = relationship(
        "RecurringTransaction",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"