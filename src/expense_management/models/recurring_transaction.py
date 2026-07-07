from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Date
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from expense_management.db.base import Base
from expense_management.models.enums import (
    RecurringFrequency,
    TransactionType,
    enum_values,
)
from expense_management.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from expense_management.models.account import Account
    from expense_management.models.category import Category
    from expense_management.models.merchant import Merchant
    from expense_management.models.user import User


class RecurringTransaction(TimestampMixin, Base):
    __tablename__ = "recurring_transactions"
    __table_args__ = (
        CheckConstraint("interval_count > 0", name="interval_count_positive"),
        CheckConstraint("amount > 0", name="amount_positive"),
        CheckConstraint(
            "ends_on IS NULL OR ends_on >= starts_on",
            name="valid_date_range",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        index=True,
        default=None,
    )

    merchant_id: Mapped[int | None] = mapped_column(
        ForeignKey("merchants.id", ondelete="SET NULL"),
        index=True,
        default=None,
    )

    transaction_type: Mapped[TransactionType] = mapped_column(
        "type",
        SQLEnum(
            TransactionType, values_callable=enum_values, native_enum=False, length=30
        ),
        nullable=False,
    )

    frequency: Mapped[RecurringFrequency] = mapped_column(
        SQLEnum(
            RecurringFrequency,
            values_callable=enum_values,
            native_enum=False,
            length=30,
        ),
        nullable=False,
    )

    interval_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    starts_on: Mapped[date] = mapped_column(Date, nullable=False)
    ends_on: Mapped[date | None] = mapped_column(Date, default=None)
    next_run_on: Mapped[date] = mapped_column(Date, index=True, nullable=False)

    description: Mapped[str | None] = mapped_column(String(255), default=None)

    user: Mapped[User] = relationship("User", back_populates="recurring_transactions")

    account: Mapped[Account] = relationship(
        "Account",
        back_populates="recurring_transactions",
    )

    category: Mapped[Category | None] = relationship(
        "Category",
        back_populates="recurring_transactions",
    )

    merchant: Mapped[Merchant | None] = relationship(
        "Merchant",
        back_populates="recurring_transactions",
    )

    def __repr__(self) -> str:
        return (
            f"RecurringTransaction(id={self.id!r}, "
            f"type={self.transaction_type!r}, "
            f"frequency={self.frequency!r})"
        )
