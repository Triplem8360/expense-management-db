from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from expense_management.core.config import settings
from expense_management.db.base import Base

# Import all models so Alembic can detect them.
import expense_management.models  # noqa: F401


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def get_context_options() -> dict:
    return {
        "target_metadata": target_metadata,
        "compare_type": True,
        "compare_server_default": True,
        "render_as_batch": settings.database_url.startswith("sqlite"),
    }


def run_migrations_offline() -> None:
    context.configure(
        url=settings.database_url,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        **get_context_options(),
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(
        settings.database_url,
        poolclass=pool.NullPool,
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            **get_context_options(),
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()