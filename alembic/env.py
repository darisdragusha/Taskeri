import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import tenant



# ───── Load environment variables ─────
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

# ───── Add app to sys.path for imports ─────
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ───── Import Base and models (this loads metadata) ─────
from app.utils.db_utils import Base
from app.models import tenant  # 👈 this will trigger all models listed in models/tenant/__init__.py

# ───── Alembic Config ─────
config = context.config

# Dynamically set the DB URL from .env
db_url = os.getenv("DB_URL")
if db_url is None:
    raise ValueError("Environment variable DB_URL is not set in .env")

config.set_main_option("sqlalchemy.url", db_url)

# Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Read schema name from CLI (e.g. `alembic -x schema=company_xyz upgrade head`)
schema_name = context.get_x_argument(as_dictionary=True).get("schema", "public")
print(f"--> Running migration for schema: '{schema_name}'")

# Provide metadata for autogenerate support
target_metadata = Base.metadata

# ───── Offline Mode ─────
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        version_table_schema=schema_name,
    )

    with context.begin_transaction():
        context.run_migrations()

# ───── Online Mode ─────
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        execution_options={"schema_translate_map": {None: schema_name}},
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=schema_name,
            include_schemas=True,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# ───── Run it ─────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
