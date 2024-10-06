import sqlite3
from backend.config import DB_PATH


def init_review_model():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
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


def get_review(review_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
        review = cursor.fetchone()
        if review:
            return {"id": review[0], "problem_id": review[1], "result": bool(review[2]), "date_created": review[3]}
        return None
    except Exception as e:
        # logger.error(f"Error in get_review {review_id}: {str(e)}", exc_info=True)
        raise e
    finally:
        conn.close()


def get_all_reviews():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM reviews")
        reviews = cursor.fetchall()
        return [
            {"id": review[0], "problem_id": review[1], "result": bool(review[2]), "date_created": review[3]}
            for review in reviews
        ]
    except Exception as e:
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
