from db.db_helpers import get_db

def get_all_reviews():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews ORDER BY date DESC')
    reviews = cursor.fetchall()
    conn.close()
    return [dict(review) for review in reviews]

def get_all_cards():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cards')
    cards = cursor.fetchall()
    conn.close()
    return [dict(card) for card in cards]

def create_card(question: str, answer: str) -> int:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cards (question, answer) VALUES (?, ?)', (question, answer))
    conn.commit()
    card_id = cursor.lastrowid
    conn.close()
    return card_id

def get_card(card_id: int) -> dict | None:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cards WHERE id = ?', (card_id,))
    card = cursor.fetchone()
    conn.close()
    return dict(card) if card else None

def create_review(card_id: int, result: bool) -> int:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reviews (card_id, result) VALUES (?, ?)', (card_id, result))
    conn.commit()
    review_id = cursor.lastrowid
    conn.close()
    return review_id

def get_review(review_id: int) -> dict | None:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews WHERE id = ?', (review_id,))
    review = cursor.fetchone()
    conn.close()
    return dict(review) if review else None
