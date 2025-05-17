from sqlalchemy import text
from sqlalchemy.orm import Session
from app.utils.migration_runner import run_alembic_for_schema

def create_new_tenant(db: Session, schema_name: str):
    db.execute(text(f"CREATE SCHEMA IF NOT EXISTS {"tenant_" + schema_name}"))
    db.commit()
    run_alembic_for_schema("tenant_" + schema_name)
