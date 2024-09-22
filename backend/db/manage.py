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
        dataframe_headers JSON,
        FOREIGN KEY (note_id) REFERENCES notes (id)           
    )
    """)

    conn.commit()
    conn.close()


import argparse


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
        for table, operations in migration_plan.items():
            for operation in operations:
                change_type, column_name, column_type = operation
                if change_type == "add_column":
                    column_name, column_type = operation[1], operation[2]
                    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column_name} {column_type}")
                else:
                    raise Exception(f"Migration type {change_type} not implemented")
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
