import logging
from .db_helpers import get_db

logger = logging.getLogger(__name__)


def delete_note(note_id: int):
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Delete related reviews first
        cursor.execute("DELETE FROM reviews WHERE note_id = ?", (note_id,))
        # Then delete the card
        cursor.execute("DELETE FROM cards WHERE note_id = ?", (note_id,))
        # Then delete the code
        cursor.execute("DELETE FROM code_completion WHERE note_id = ?", (note_id,))
        # Then delete the note
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Error in delete_note for note {note_id}: {str(e)}", exc_info=True)
        raise e
    finally:
        conn.close()


def delete_review(review_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Delete related reviews first
        cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Error in delete_review {review_id}: {str(e)}", exc_info=True)
        raise e
    finally:
        conn.close()


def get_all_reviews():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews ORDER BY date DESC")
    reviews = cursor.fetchall()
    conn.close()
    return [dict(review) for review in reviews]


def create_review(note_id: int, result: bool) -> int:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (note_id, result) VALUES (?, ?)", (note_id, result))
    conn.commit()
    review_id = cursor.lastrowid
    conn.close()
    return review_id


def get_review(review_id: int) -> dict | None:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
    review = cursor.fetchone()
    conn.close()
    return dict(review) if review else None
