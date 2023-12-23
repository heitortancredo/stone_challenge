import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from infrastructure.postgresql import DATABASE_URL
from models import *  # noqa
from models import BaseModel

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configurations = config.get_section(config.config_ini_section)
    configurations["sqlalchemy.url"] = DATABASE_URL

    connectable = engine_from_config(
        configurations,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()