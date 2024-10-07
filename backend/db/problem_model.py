import json
import sqlite3
from backend.code_completion.check_code import get_pandas_header, get_preprocessing_headers
from backend.config import DB_PATH


# Initialize the database
def init_problem_model():
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


def get_all_problem_ids():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT p.id
    FROM problems p
    """
    cursor.execute(query)
    problem_ids = cursor.fetchall()
    conn.close()
    return problem_ids


def get_problem_for_polars(problem_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = f"""
    SELECT p.id, p.description, c.code, c.preprocessing_code, c.default_code, d.dataset_name, d.dataset_headers
    FROM problems p
    JOIN code c ON p.id = c.problem_id
    JOIN datasets d ON p.id = d.problem_id
    WHERE p.id == {problem_id}
    ORDER BY p.id
    LIMIT 1
    """

    cursor.execute(query)
    result = cursor.fetchone()

    problem_id, description, code, preprocessing_code, default_code, dataset_name, dataset_headers = result

    return {
        "problem_id": problem_id,
        "description": description,
        "code": code,
        "preprocessing_code": preprocessing_code,
        "default_code": default_code,
        "dataset_name": dataset_name,
        "dataset_headers": dataset_headers,
    }


def delete_problem(problem_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Start a transaction
        cursor.execute("BEGIN TRANSACTION")

        # Delete associated datasets
        cursor.execute("DELETE FROM datasets WHERE problem_id = ?", (problem_id,))

        # Delete associated code
        cursor.execute("DELETE FROM code WHERE problem_id = ?", (problem_id,))

        # Delete the problem
        cursor.execute("DELETE FROM problems WHERE id = ?", (problem_id,))

        # Commit the transaction
        conn.commit()
        print(f"Problem with id {problem_id} and its associated data have been deleted.")

    except sqlite3.Error as e:
        # If an error occurs, roll back the transaction
        conn.rollback()
        print(f"An error occurred while deleting the problem: {e}")

    finally:
        # Close the database connection
        conn.close()


def add_new_polars_problem(code, problem_description, datasets, preprocessing_code, code_start):
    # Get the dataframe headers
    headers = {}
    for dataset in datasets:
        headers[dataset.replace(".csv", "")] = get_pandas_header(dataset)

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
        for dataset in datasets:
            dataset_header = json.dumps(get_pandas_header(dataset))
            new_cursor.execute(
                """
            INSERT INTO datasets (problem_id, dataset_name, dataset_headers)
            VALUES (?, ?, ?)
            """,
                (problem_id, dataset.replace(".csv", ""), dataset_header),
            )
        # Get preprocessing headers
        if preprocessing_code != "":
            preprocessing_header = json.dumps(get_preprocessing_headers(datasets, preprocessing_code))
            new_cursor.execute(
                """
            INSERT INTO datasets (problem_id, dataset_name, dataset_headers)
            VALUES (?, ?, ?)
            """,
                (problem_id, "preprocessing", preprocessing_header),
            )

        # Commit the changes
        new_conn.commit()

        print(f"Inserted data for problem_id: {problem_id}")

    except sqlite3.Error as e:
        print(f"An error occurred while inserting data: {e}")

    finally:
        # Close the new database connection
        new_conn.close()
