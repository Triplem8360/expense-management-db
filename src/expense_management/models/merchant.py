from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from expense_management.db.base import Base
from expense_management.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from expense_management.models.recurring_transaction import RecurringTransaction
    from expense_management.models.transaction import Transaction
    from expense_management.models.user import User


class Merchant(TimestampMixin, Base):
    __tablename__ = "merchants"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_merchants_user_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    website: Mapped[str | None] = mapped_column(String(255), default=None)
    notes: Mapped[str | None] = mapped_column(String(500), default=None)

    user: Mapped[User] = relationship("User", back_populates="merchants")

    transactions: Mapped[list[Transaction]] = relationship(
        "Transaction",
        back_populates="merchant",
    )

    recurring_transactions: Mapped[list[RecurringTransaction]] = relationship(
        "RecurringTransaction",
        back_populates="merchant",
    )

    def __repr__(self) -> str:
        return f"Merchant(id={self.id!r}, name={self.name!r})"
