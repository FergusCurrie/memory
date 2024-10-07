import json
import logging
import sqlite3
from backend.code_execution.utils import get_pandas_header, get_preprocessing_headers
from backend.config import DB_PATH

logger = logging.getLogger(__name__)


# Initialize the database
def init_problem_model():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create problems table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        type TEXT,
        status TEXT,
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
    SELECT p.id, p.status
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
    SELECT p.id, p.description, p.type, c.code, c.preprocessing_code, c.default_code, d.dataset_name, d.dataset_headers
    FROM problems p
    JOIN code c ON p.id = c.problem_id
    JOIN datasets d ON p.id = d.problem_id
    WHERE p.id == {problem_id}
    """
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        return None

    problem_id, description, problem_type, code, preprocessing_code, default_code = results[0][:6]
    datasets = {row[6]: json.loads(row[7]) for row in results}

    result = {
        "problem_id": problem_id,
        "type": problem_type,
        "description": description,
        "code": code,
        "preprocessing_code": preprocessing_code,
        "default_code": default_code,
        "datasets": datasets
    }

    # logger.info(result)
    return result

    # cursor.execute(query)
    # result = cursor.fetchall()

    # logger.info(f'fetching all somehow has big thing: {len(result)} for {problem_id}')

    # problem_id, description, problem_type, code, preprocessing_code, default_code, dataset_name, dataset_headers = (
    #     result[0]
    # )
   

    
    # result =  {
    #     "problem_id": problem_id,
    #     "type": problem_type,
    #     "description": description,
    #     "code": code,
    #     "preprocessing_code": preprocessing_code,
    #     "default_code": default_code,
    #     "dataset_name": dataset_name,
    #     "dataset_headers": dataset_headers,
    # }
    
    # return result 

def toggle_suspend_problem(problem_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Get the current status of the problem
        cursor.execute("SELECT status FROM problems WHERE id = ?", (problem_id,))
        current_status = cursor.fetchone()[0]

        # Toggle the status
        new_status = 'suspended' if current_status == 'active' else 'active'

        # Update the problem's status
        cursor.execute(
            """
            UPDATE problems
            SET status = ?
            WHERE id = ?
            """,
            (new_status, problem_id)
        )

        # Commit the changes
        conn.commit()
        print(f"Problem with id {problem_id} has been toggled to {new_status}.")

    except sqlite3.Error as e:
        # If an error occurs, roll back the changes
        conn.rollback()
        print(f"An error occurred while toggling the problem status: {e}")

    finally:
        # Close the database connection
        conn.close()

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


def add_new_polars_problem(code, problem_description, datasets, preprocessing_code, code_start, type):
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
        INSERT INTO problems (description, type)
        VALUES (?, ?)
        """,
            (problem_description, type),
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

        logger.info(f"Inserted data for problem_id: {problem_id}")

    except sqlite3.Error as e:
        logger.info(f"An error occurred while inserting data: {e}")

    finally:
        # Close the new database connection
        new_conn.close()


def update_problem_in_db(problem_id: int, problem: dict):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Update problems table
        cursor.execute(
            """
            UPDATE problems
            SET description = ?
            WHERE id = ?
            """,
            (problem.get('description'), problem_id)
        )

        # Update code table
        cursor.execute(
            """
            UPDATE code
            SET code = ?
            WHERE problem_id = ?
            """,
            (problem.get('code'), problem_id)
        )

        conn.commit()
        logger.info(f"Updated data for problem_id: {problem_id}")

        # Fetch and return the updated problem
        return get_problem_for_polars(problem_id)

    except sqlite3.Error as e:
        logger.error(f"An error occurred while updating data: {e}")
        conn.rollback()
        return None

    finally:
        conn.close()
