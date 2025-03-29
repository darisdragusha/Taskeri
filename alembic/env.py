import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ───── Load environment variables ─────
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

# ───── Add app to sys.path for import ─────
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ───── Import Base and models ─────
from app.utils.db_utils import Base
from app.models import *

# ───── Alembic Config ─────
config = context.config

# Dynamically set the DB URL from .env
db_url = os.getenv("DB_URL")

if db_url is None:
    raise ValueError("Environment variable DB_URL is not set in your .env file")

config.set_main_option("sqlalchemy.url", db_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Let Alembic know about your models' metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True  # Tracks column type changes too
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
