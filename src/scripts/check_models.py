from __future__ import annotations

import expense_management.models
from expense_management.db.base import Base


def main() -> None:
    print("Registered tables:")
    for table_name in sorted(Base.metadata.tables):
        print(f"- {table_name}")


if __name__ == "__main__":
    main()
