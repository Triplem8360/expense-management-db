from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from expense_management.db.base import Base
from expense_management.models.enums import BudgetPeriod, enum_values
from expense_management.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from expense_management.models.category import Category
    from expense_management.models.user import User


class Budget(TimestampMixin, Base):
    __tablename__ = "budgets"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "category_id",
            "period",
            "starts_on",
            name="uq_budgets_user_category_period_start",
        ),
        CheckConstraint("limit_amount > 0", name="limit_amount_positive"),
        CheckConstraint(
            "alert_threshold_percent >= 0 AND alert_threshold_percent <= 100",
            name="alert_threshold_percent_range",
        ),
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

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        index=True,
        default=None,
    )

    period: Mapped[BudgetPeriod] = mapped_column(
        SQLEnum(
            BudgetPeriod, values_callable=enum_values, native_enum=False, length=30
        ),
        nullable=False,
    )

    starts_on: Mapped[date] = mapped_column(Date, nullable=False)
    ends_on: Mapped[date | None] = mapped_column(Date, default=None)

    limit_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)

    alert_threshold_percent: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("80.00"),
    )

    user: Mapped[User] = relationship("User", back_populates="budgets")

    category: Mapped[Category | None] = relationship(
        "Category",
        back_populates="budgets",
    )

    def __repr__(self) -> str:
        return f"Budget(id={self.id!r}, period={self.period!r}, limit={self.limit_amount!r})"
