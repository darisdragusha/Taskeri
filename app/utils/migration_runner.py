import subprocess

def run_alembic_for_schema(schema_name: str):
    from app.utils.env_utils import EnvironmentVariable, get_env
    print(f"Running Alembic migration for tenant schema: {schema_name}")

    # Pass database name when in test environment
    extra_args = []
    if get_env(EnvironmentVariable.TESTING) == 'true':
        db_name = 'taskeri_test'
        extra_args.append("-x")
        extra_args.append(f"db_name={db_name}")

    result = subprocess.run(
        ["alembic", "-x", f"schema={schema_name}"] + extra_args + ["upgrade", "head"],
        capture_output=True,
        text=True
    )

    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)

    if result.returncode != 0:
        print("Alembic Migration Failed!")
        raise RuntimeError(f"Migration failed:\n{result.stderr}")

    print(f"Migration complete for schema: {schema_name}")
