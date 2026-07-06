from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from expense_management.db.base import Base
from expense_management.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from expense_management.models.budget import Budget
    from expense_management.models.recurring_transaction import RecurringTransaction
    from expense_management.models.transaction_split import TransactionSplit
    from expense_management.models.user import User


class Category(TimestampMixin, Base):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("user_id", "name", "parent_id", name="uq_categories_user_name_parent"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
            index=True,
        default=None,
    )

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    color: Mapped[str | None] = mapped_column(String(20), default=None)
    icon: Mapped[str | None] = mapped_column(String(80), default=None)

    user: Mapped[User] = relationship("User", back_populates="categories")

    parent: Mapped[Category | None] = relationship(
        "Category",
        remote_side=[id],
        back_populates="children",
    )

    children: Mapped[list[Category]] = relationship(
        "Category",
        back_populates="parent",
    )

    splits: Mapped[list[TransactionSplit]] = relationship(
        "TransactionSplit",
        back_populates="category",
    )

    budgets: Mapped[list[Budget]] = relationship(
        "Budget",
        back_populates="category",
    )

    recurring_transactions: Mapped[list[RecurringTransaction]] = relationship(
        "RecurringTransaction",
        back_populates="category",
    )

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r}, parent_id={self.parent_id!r})"