from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from expense_management.db.base import Base
from expense_management.models.enums import RecurringFrequency, TransactionType, enum_values
from expense_management.models.mixins import TimestampMixin


class RecurringTransaction(TimestampMixin, Base):
    __tablename__ = "recurring_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    merchant_id: Mapped[int | None] = mapped_column(ForeignKey("merchants.id", ondelete="SET NULL"))
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, values_callable=enum_values, native_enum=False, length=30),
        nullable=False,
    )
    frequency: Mapped[RecurringFrequency] = mapped_column(
        Enum(RecurringFrequency, values_callable=enum_values, native_enum=False, length=30),
        nullable=False,
    )
    interval_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    starts_on: Mapped[date] = mapped_column(Date, nullable=False)
    ends_on: Mapped[date | None] = mapped_column(Date)
    next_run_on: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))

    user = relationship("User", back_populates="recurring_transactions")
    account = relationship("Account")
    category = relationship("Category", back_populates="recurring_transactions")
    merchant = relationship("Merchant")
