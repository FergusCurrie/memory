import sqlite3
from backend.config import DB_PATH


def delete_review(review_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Delete related reviews first
        cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        # logger.error(f"Error in delete_review {review_id}: {str(e)}", exc_info=True)
        raise e
    finally:
        conn.close()


def add_review(problem_id, result):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
        INSERT INTO reviews (problem_id, result)
        VALUES (?, ?)
        """,
            (problem_id, result),
        )

        review_id = cursor.lastrowid
        conn.commit()
        return review_id
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()


def delete_problem():
    # must delete connected problems

    pass


def get_problem_for_polars(problem_id):
    conn = sqlite3.connect(DB_PATH)
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


def insert(code, problem_description, dataset_name, preprocessing_code, code_start, dataset_headers):
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
