from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum as SQLEnum
from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from expense_management.db.base import Base
from expense_management.models.enums import AccountStatus, AccountType, enum_values
from expense_management.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from expense_management.models.recurring_transaction import RecurringTransaction
    from expense_management.models.transaction import Transaction
    from expense_management.models.user import User


class Account(TimestampMixin, Base):
    __tablename__ = "accounts"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_accounts_user_name"),
        CheckConstraint("length(currency) = 3", name="currency_length"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(120), nullable=False)

    account_type: Mapped[AccountType] = mapped_column(
        "type",
        SQLEnum(AccountType, values_callable=enum_values, native_enum=False, length=30),
        nullable=False,
    )

    status: Mapped[AccountStatus] = mapped_column(
        SQLEnum(
            AccountStatus, values_callable=enum_values, native_enum=False, length=30
        ),
        nullable=False,
        default=AccountStatus.ACTIVE,
    )

    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    opening_balance: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    institution_name: Mapped[str | None] = mapped_column(String(120), default=None)
    masked_number: Mapped[str | None] = mapped_column(String(20), default=None)

    user: Mapped[User] = relationship("User", back_populates="accounts")

    transactions: Mapped[list[Transaction]] = relationship(
        "Transaction",
        back_populates="account",
        foreign_keys="Transaction.account_id",
    )

    transfer_transactions: Mapped[list[Transaction]] = relationship(
        "Transaction",
        back_populates="transfer_account",
        foreign_keys="Transaction.transfer_account_id",
    )

    recurring_transactions: Mapped[list[RecurringTransaction]] = relationship(
        "RecurringTransaction",
        back_populates="account",
    )

    def __repr__(self) -> str:
        return (
            f"Account(id={self.id!r}, name={self.name!r}, type={self.account_type!r})"
        )
