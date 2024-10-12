import sqlite3
import logging
from backend.config import DB_PATH

logger = logging.getLogger(__name__)

def init_card_model():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create cards table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER,
        front TEXT,
        back TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (problem_id) REFERENCES problems (id)
    )
    """)

    conn.commit()
    conn.close()

def add_card(front, back):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Insert into problems table
        cursor.execute(
            """
        INSERT INTO problems (description, type)
        VALUES (?, ?)
        """,
            (front, 'card'),
        )
        problem_id = cursor.lastrowid

        cursor.execute("""
        INSERT INTO cards (problem_id, front, back)
        VALUES (?, ?, ?)
        """, (problem_id, front, back))

        conn.commit()
        logger.info(f"Added new card for problem_id: {problem_id}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        logger.error(f"An error occurred while adding a card: {e}")
        return None
    finally:
        conn.close()

def get_card_by_problem_id(problem_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT id, problem_id, front, back, created_at
        FROM cards
        WHERE problem_id = ?
        """, (problem_id,))

        card = cursor.fetchone()
        if card:
            return {
                "id": card[0],
                "problem_id": card[1],
                "front": card[2],
                "back": card[3],
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
    #init_card_model()
    add_card('Card Front', 'Card Back')
