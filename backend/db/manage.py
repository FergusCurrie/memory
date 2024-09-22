import argparse
import json
import os
import sqlite3
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from backend.config import DB_PATH


# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Notes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tags JSON DEFAULT '{}',
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create Review table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note_id INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        result BOOLEAN,
        FOREIGN KEY (note_id) REFERENCES notes (id)
    )
    """)

    # Create Card table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note_id INTEGER,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        FOREIGN KEY (note_id) REFERENCES notes (id)
    )
    """)

    # Create Code Completion table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS code_completion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note_id INTEGER,
        code TEXT,
        problem_description TEXT,
        dataset_name TEXT,
        preprocessing_code TEXT,
        code_start text DEFAULT NULL,
        dataset_headers JSON,
        FOREIGN KEY (note_id) REFERENCES notes (id)           
    )
    """)

    conn.commit()
    conn.close()


def rename_column(cursor, table, old_column_name, new_column_name):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()

    # Create new table with renamed column
    new_columns = [f"{new_column_name if col[1] == old_column_name else col[1]} {col[2]}" for col in columns]
    print(new_columns)
    cursor.execute(f"CREATE TABLE new_{table} ({', '.join(new_columns)})")

    # Copy data from old table to new table
    old_cols = [col[1] for col in columns]
    new_cols = [new_column_name if col == old_column_name else col for col in old_cols]
    cursor.execute(f"INSERT INTO new_{table} ({', '.join(new_cols)}) SELECT {', '.join(old_cols)} FROM {table}")

    # Drop old table and rename new table
    cursor.execute(f"DROP TABLE {table}")
    cursor.execute(f"ALTER TABLE new_{table} RENAME TO {table}")


def update_dataset_header_rows(cursor, table):
    cursor.execute(f"SELECT id, dataset_name, dataset_header FROM {table}")
    rows = cursor.fetchall()
    for row in rows:
        id, dataset_name, dataset_headers = row

        # Create a new JSON object with dataset_name as key and dataset_headers as value
        new_headers = json.dumps({dataset_name.replace(".csv", ""): dataset_headers})

        # Update the row with the new JSON format
        cursor.execute(f"UPDATE {table} SET dataset_header = ? WHERE id = ?", (new_headers, id))

    print(f"Updated {len(rows)} rows in the {table} table.")


def update_solution_code(cursor, table):
    cursor.execute(f"SELECT id, code, dataset_name FROM {table}")
    rows = cursor.fetchall()
    for row in rows:
        id, code, dataset = row

        # Update the row with the new JSON format
        cursor.execute(
            f"UPDATE {table} SET code = ? WHERE id = ?", (code.replace("df", dataset.replace(".csv", "")), id)
        )

    print(f"Updated {len(rows)} rows in the {table} table.")


def run_migration():
    # Add your migration logic here
    print("Running migration...")
    with open("backend/db/migration.json", "r") as f:
        migration_plan = json.load(f)
    print(migration_plan)
    # Example: Add a new column to an existing table
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE code_completion ADD COLUMN code_start TEXT DEFAULT NULL")
        cursor.execute("ALTER TABLE code_completion ADD COLUMN preprocessing_code TEXT DEFAULT ''")
        update_dataset_header_rows(cursor, "code_completion")
        update_solution_code(cursor, "code_completion")
        rename_column(cursor, "code_completion", "dataset_header", "dataset_headers")

        # for table, operations in migration_plan.items():
        #     for operation in operations:
        #         change_type, column_name, column_type = operation
        #         if change_type == "add_column":
        #             column_name, column_type = operation[1], operation[2]
        #             cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column_name} {column_type}")
        #         else:
        #             raise Exception(f"Migration type {change_type} not implemented")
        # cursor.execute("ALTER TABLE code_completion ADD COLUMN preprocessing_code TEXT")
        print("Migration completed successfully.")
    except sqlite3.OperationalError as e:
        print(f"Migration failed: {e}")
    finally:
        conn.commit()
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database management script")
    parser.add_argument("action", choices=["init", "migrate"], help="Action to perform: init_db or run_migration")

    args = parser.parse_args()

    if args.action == "init":
        init_db()
        print("Database initialized successfully.")
    elif args.action == "migrate":
        run_migration()
    else:
        print("No arguments supplied ")

init_db()
