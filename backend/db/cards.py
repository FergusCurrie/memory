import logging
from .db_helpers import get_db

logger = logging.getLogger(__name__)


def update_card_in_db(card_id: int, question: str, answer: str):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE cards SET question = ?, answer = ? WHERE id = ?", (question, answer, card_id))
        conn.commit()
        # Fetch the updated card
        cursor.execute("SELECT id, question, answer FROM cards WHERE id = ?", (card_id,))
        updated_card = cursor.fetchone()

        if updated_card is None:
            raise ValueError(f"Card with id {card_id} not found")

        return {"id": updated_card[0], "question": updated_card[1], "answer": updated_card[2]}
    except Exception as e:
        conn.rollback()
        logger.error(f"Error in update_card_in_db for card {card_id}: {str(e)}", exc_info=True)
        raise e
    finally:
        conn.close()


def get_all_cards():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards")
    cards = cursor.fetchall()
    conn.close()
    return [dict(card) for card in cards]


def create_card(card):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes DEFAULT VALUES")
    note_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO cards (note_id, question, answer) VALUES (?, ?, ?)", (note_id, card.question, card.answer)
    )
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


def get_note_id_from_card_id(card_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
    card = cursor.fetchone()
    conn.close()
    return dict(card)["note_id"] if card else None
