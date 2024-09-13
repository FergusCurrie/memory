import sqlite3
from backend.config import DB_PATH


# Helper function to get a database connection
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def print_all_records():
    conn = get_db()
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"\n--- Records in {table_name} table ---")

        # Get all records from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()

        if records:
            # Print column names
            column_names = [description[0] for description in cursor.description]
            print(" | ".join(column_names))
            print("-" * (len(" | ".join(column_names))))

            # Print records
            for record in records:
                print(" | ".join(str(field) for field in record))
        else:
            print("No records found.")

    conn.close()


if __name__ == "__main__":
    print_all_records()
