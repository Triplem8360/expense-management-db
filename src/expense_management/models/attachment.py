from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from expense_management.db.base import Base
from expense_management.models.enums import AttachmentType, enum_values
from expense_management.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from expense_management.models.transaction import Transaction


class Attachment(TimestampMixin, Base):
    __tablename__ = "attachments"
    __table_args__ = (
        CheckConstraint("size_bytes IS NULL OR size_bytes >= 0", name="size_bytes_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("transactions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    attachment_type: Mapped[AttachmentType] = mapped_column(
        "type",
        SQLEnum(AttachmentType, values_callable=enum_values, native_enum=False, length=30),
        nullable=False,
        default=AttachmentType.RECEIPT,
    )

    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(120), default=None)
    size_bytes: Mapped[int | None] = mapped_column(Integer, default=None)

    transaction: Mapped[Transaction] = relationship(
        "Transaction",
        back_populates="attachments",
    )

    def __repr__(self) -> str:
        return f"Attachment(id={self.id!r}, file_name={self.file_name!r})"