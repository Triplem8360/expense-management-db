from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from expense_management.db.base import Base
from expense_management.models.association import transaction_tags
from expense_management.models.enums import (
    TransactionStatus,
    TransactionType,
    enum_values,
)
from expense_management.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from expense_management.models.account import Account
    from expense_management.models.attachment import Attachment
    from expense_management.models.merchant import Merchant
    from expense_management.models.tag import Tag
    from expense_management.models.transaction_split import TransactionSplit
    from expense_management.models.user import User


class Transaction(TimestampMixin, Base):
    __tablename__ = "transactions"
    __table_args__ = (CheckConstraint("amount > 0", name="amount_positive"),)

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

    transfer_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id", ondelete="SET NULL"),
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

    status: Mapped[TransactionStatus] = mapped_column(
        SQLEnum(
            TransactionStatus, values_callable=enum_values, native_enum=False, length=30
        ),
        nullable=False,
        default=TransactionStatus.PENDING,
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    occurred_on: Mapped[date] = mapped_column(Date, index=True, nullable=False)

    description: Mapped[str | None] = mapped_column(String(255), default=None)
    notes: Mapped[str | None] = mapped_column(Text, default=None)
    external_reference: Mapped[str | None] = mapped_column(String(120), default=None)

    user: Mapped[User] = relationship("User", back_populates="transactions")

    account: Mapped[Account] = relationship(
        "Account",
        back_populates="transactions",
        foreign_keys=[account_id],
    )

    transfer_account: Mapped[Account | None] = relationship(
        "Account",
        back_populates="transfer_transactions",
        foreign_keys=[transfer_account_id],
    )

    merchant: Mapped[Merchant | None] = relationship(
        "Merchant",
        back_populates="transactions",
    )

    splits: Mapped[list[TransactionSplit]] = relationship(
        "TransactionSplit",
        back_populates="transaction",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    tags: Mapped[list[Tag]] = relationship(
        "Tag",
        secondary=transaction_tags,
        back_populates="transactions",
    )

    attachments: Mapped[list[Attachment]] = relationship(
        "Attachment",
        back_populates="transaction",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"Transaction(id={self.id!r}, type={self.transaction_type!r}, amount={self.amount!r})"
