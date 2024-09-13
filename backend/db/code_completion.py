from .db_helpers import get_db


def get_a_code_completition(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM code_completion WHERE id = ?", (id,))
    code = cursor.fetchone()
    conn.close()
    return dict(code) if code else None


def get_all_codes():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM code_completion")
    codes = cursor.fetchall()
    conn.close()
    return [dict(code) for code in codes]


def get_note_id_from_code_id(code_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM code_completion WHERE id = ?", (code_id,))
    card = cursor.fetchone()
    conn.close()
    return dict(card)["note_id"] if card else None
