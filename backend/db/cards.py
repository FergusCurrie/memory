import logging
from db.db_helpers import get_db

logger = logging.getLogger(__name__)


def delete_card_and_reviews(card_id: int):
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Delete related reviews first
        cursor.execute("DELETE FROM reviews WHERE card_id = ?", (card_id,))
        # Then delete the card
        cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Error in delete_card_and_reviews for card {card_id}: {str(e)}", exc_info=True)
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


def get_all_cards():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards")
    cards = cursor.fetchall()
    conn.close()
    return [dict(card) for card in cards]


def create_card(question: str, answer: str) -> int:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cards (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    card_id = cursor.lastrowid
    conn.close()
    return card_id


def get_card(card_id: int) -> dict | None:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
    card = cursor.fetchone()
    conn.close()
    return dict(card) if card else None


def create_review(card_id: int, result: bool) -> int:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (card_id, result) VALUES (?, ?)", (card_id, result))
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
