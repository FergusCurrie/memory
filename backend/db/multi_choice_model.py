import sqlite3
import logging
from backend.config import DB_PATH

logger = logging.getLogger(__name__)

def init_multi_choice_model():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create cards table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS multi_choice (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER,
        description TEXT,
        generation_code TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (problem_id) REFERENCES problems (id)
    )
    """)

    conn.commit()
    conn.close()

def add_multi_choice(description, generation_code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Insert into problems table
        cursor.execute(
            """
        INSERT INTO problems (description, type)
        VALUES (?, ?)
        """,
            (description, 'multi_choice'),
        )
        problem_id = cursor.lastrowid

        cursor.execute("""
        INSERT INTO multi_choice (problem_id, description, generation_code)
        VALUES (?, ?, ?)
        """, (problem_id, description, generation_code))

        conn.commit()
        logger.info(f"Added new multi choice for problem_id: {problem_id}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        logger.error(f"An error occurred while adding a card: {e}")
        return None
    finally:
        conn.close()

def get_multi_choice_by_problem_id(problem_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT id, problem_id, description, generation_code, created_at
        FROM multi_choice
        WHERE problem_id = ?
        """, (problem_id,))

        card = cursor.fetchone()
        if card:
            return {
                "id": card[0],
                "problem_id": card[1],
                "description": card[2],
                "generation_code": card[3],
                "created_at": card[4]
            }
        else:
            return None
    except sqlite3.Error as e:
        logger.error(f"An error occurred while fetching a card: {e}")
        return None
    finally:
        conn.close()

# You can add more functions here as needed, such as update_card, delete_card, etc.

if __name__ == "__main__":
    init_multi_choice_model()
    add_multi_choice(
        "Given two points: {input_1}, {input_2}. Which of the following are affine combinations: 1:{option_1}, 2:{option_2}, 3:{option_3}, 4:{option_4}", 
        "input_1 = (1,2)\ninput_2 = (2,3)\noption_1 = (5,6)\noption_2 = (3,9)\noption_3 = (2,8)\noption_4 = (1,7)\ncorrect_answer=(1,7)"
    )