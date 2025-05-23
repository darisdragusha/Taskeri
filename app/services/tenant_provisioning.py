from sqlalchemy import text
from sqlalchemy.orm import Session
from app.utils.migration_runner import run_alembic_for_schema

def create_new_tenant(db: Session, schema_name: str):
    from app.utils.env_utils import EnvironmentVariable, get_env
    # Make sure we always use the tenant_ prefix consistently
    tenant_schema = schema_name if schema_name.startswith("tenant_") else f"tenant_{schema_name}"
    
    # Create the schema within the current database
    db.execute(text(f"CREATE SCHEMA IF NOT EXISTS {tenant_schema}"))
    db.commit()
    
    # Run migrations on the new schema
    # In test mode, explicitly pass the test database name
    if get_env(EnvironmentVariable.TESTING) == 'true':
        print(f"Running migrations for test tenant schema: {tenant_schema}")
        # For tests, create tables directly without alembic
        # This is more reliable in tests and avoids the database vs schema confusion
        from app.utils.db_utils import Base
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        # Get a fresh engine using the test database
        test_db_url = (
            f"mysql+mysqlconnector://{get_env(EnvironmentVariable.DB_USERNAME)}:"
            f"{get_env(EnvironmentVariable.DB_PASSWORD)}@"
            f"{get_env(EnvironmentVariable.DB_HOST)}:"
            f"{get_env(EnvironmentVariable.DB_PORT)}/"
            f"taskeri_test"
        )
        test_engine = create_engine(test_db_url)
        
        # Create a connection to run schema-specific SQL
        with test_engine.connect() as connection:
            # Create the schema if it doesn't exist
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {tenant_schema}"))
            connection.commit()
            
            # Use the schema
            connection.execute(text(f"USE {tenant_schema}"))
            
            # Create all tenant-specific tables in this schema
            # Filter out tables that belong to global schema
            tables = [table for table in Base.metadata.sorted_tables 
                     if not table.schema or table.schema != 'taskeri_global']
            
            # Temporarily set schema for all tables to this tenant schema
            for table in tables:
                table.schema = tenant_schema
            
            # Create the tables
            Base.metadata.create_all(bind=connection, tables=tables)
            connection.commit()
            
            # Reset schemas to avoid side effects
            for table in tables:
                table.schema = None
    else:
        # Regular environment - use Alembic as before
        run_alembic_for_schema(tenant_schema)
