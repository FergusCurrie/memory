from .db_helpers import get_db
from ..code_completion.check_code import get_pandas_header

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

def add_code_problem_to_db(description, dataset_path, code):
    header = get_pandas_header(dataset_path)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes DEFAULT VALUES")
    note_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO code_completion (note_id, problem_description, dataset_name, code, dataset_header) VALUES (?, ?, ?, ?, ?)",
        (note_id, description, dataset_path, code, header),
    )
    conn.commit()
    conn.close()
    return note_id
