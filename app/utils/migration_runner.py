import subprocess

def run_alembic_for_schema(schema_name: str):
    print(f"Running Alembic migration for tenant schema: {schema_name}")

    result = subprocess.run(
        ["alembic", "-x", f"schema={schema_name}", "upgrade", "head"],
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
