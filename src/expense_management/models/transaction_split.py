from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from expense_management.db.base import Base
from expense_management.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from expense_management.models.category import Category
    from expense_management.models.transaction import Transaction


class TransactionSplit(TimestampMixin, Base):
    __tablename__ = "transaction_splits"
    __table_args__ = (
        UniqueConstraint(
            "transaction_id",
            "category_id",
            name="uq_transaction_splits_transaction_category",
        ),
        CheckConstraint("amount > 0", name="amount_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("transactions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    memo: Mapped[str | None] = mapped_column(String(255), default=None)

    transaction: Mapped[Transaction] = relationship(
        "Transaction",
        back_populates="splits",
    )

    category: Mapped[Category] = relationship(
        "Category",
        back_populates="splits",
    )

    def __repr__(self) -> str:
        return (
            f"TransactionSplit(id={self.id!r}, "
            f"transaction_id={self.transaction_id!r}, "
            f"category_id={self.category_id!r}, "
            f"amount={self.amount!r})"
        )