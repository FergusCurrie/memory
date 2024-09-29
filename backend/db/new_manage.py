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

    # Create problems table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # code
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS code (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER,
        code TEXT,
        preprocessing_code TEXT,
        default_code TEXT,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (problem_id) REFERENCES problems (id)
    )
    """)

    # datasets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER,
        dataset_name TEXT,
        dataset_headers JSON,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (problem_id) REFERENCES problems (id)
    )
    """)

    # Create Review table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER,
        result BOOLEAN,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (problem_id) REFERENCES problems (id)
    )
    """)

    conn.commit()
    conn.close()


def print_first_code_completion_row():
    # Connect to the old database
    old_conn = sqlite3.connect("old_flashcards.db")
    old_cursor = old_conn.cursor()

    try:
        # Execute a query to fetch the first row from code_completion table
        old_cursor.execute("SELECT * FROM code_completion LIMIT 1")

        # Fetch the first row
        first_row = old_cursor.fetchone()
        id, note_id, code, problem_description, dataset_name, preprocessing_code, code_start, dataset_headers = (
            first_row
        )

        # Connect to the new database
        new_conn = sqlite3.connect(DB_PATH)
        new_cursor = new_conn.cursor()

        try:
            # Insert into problems table
            new_cursor.execute(
                """
            INSERT INTO problems (description)
            VALUES (?)
            """,
                (problem_description,),
            )
            problem_id = new_cursor.lastrowid

            # Insert into code table
            new_cursor.execute(
                """
            INSERT INTO code (problem_id, code, preprocessing_code, default_code)
            VALUES (?, ?, ?, ?)
            """,
                (problem_id, code, preprocessing_code, code_start),
            )

            # Insert into datasets table
            new_cursor.execute(
                """
            INSERT INTO datasets (problem_id, dataset_name, dataset_headers)
            VALUES (?, ?, ?)
            """,
                (problem_id, dataset_name, dataset_headers),
            )

            # Commit the changes
            new_conn.commit()

            print(f"Inserted data for problem_id: {problem_id}")

        except sqlite3.Error as e:
            print(f"An error occurred while inserting data: {e}")

        finally:
            # Close the new database connection
            new_conn.close()

        print(type(first_row))

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        old_conn.close()


def get_code_for_first_problem():
    try:
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()

        query = """
        SELECT p.id, p.description, c.code, c.preprocessing_code, c.default_code, d.dataset_name, d.dataset_headers
        FROM problems p
        JOIN code c ON p.id = c.problem_id
        JOIN datasets d ON p.id = d.problem_id
        ORDER BY p.id
        LIMIT 1
        """

        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            problem_id, description, code, preprocessing_code, default_code, dataset_name, dataset_headers = result
            print(
                {
                    "problem_id": problem_id,
                    "description": description,
                    "code": code,
                    "preprocessing_code": preprocessing_code,
                    "default_code": default_code,
                    "dataset_name": dataset_name,
                    "dataset_headers": dataset_headers,
                }
            )
        return

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # Call the function to print the first row
    # init_db()
    # print_first_code_completion_row()
    get_code_for_first_problem()
