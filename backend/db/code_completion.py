import json
import logging
from ..code_completion.check_code import get_pandas_header, get_preprocessing_headers
from .db_helpers import get_db

logger = logging.getLogger(__name__)


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


def add_code_problem_to_db(description, datasets, code, preprocessing_code, default_code):
    # Get the dataframe headers
    headers = {}
    for dataset in datasets:
        headers[dataset.replace(".csv", "")] = get_pandas_header(dataset)
    # Get preprocessing headers
    if preprocessing_code != "":
        headers["preprocessing"] = get_preprocessing_headers(datasets, preprocessing_code)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes DEFAULT VALUES")
    note_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO code_completion (note_id, problem_description, dataset_name, code, preprocessing_code, dataset_headers, code_start) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (note_id, description, ",".join(datasets), code, preprocessing_code, json.dumps(headers), default_code),
    )
    conn.commit()
    conn.close()
    return note_id


def update_code_in_db(code_id: int, dataset_name: str, problem_description: str, code: str):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE code_completion SET dataset_name = ?, problem_description = ?, code = ? WHERE id = ?",
            (dataset_name, problem_description, code, code_id),
        )
        conn.commit()
        # Fetch the updated card
        cursor.execute("SELECT id, dataset_name, problem_description FROM code_completion WHERE id = ?", (code_id,))
        updated_card = cursor.fetchone()

        if updated_card is None:
            raise ValueError(f"Code with id {code_id} not found")

        return {"id": updated_card[0]}
    except Exception as e:
        conn.rollback()
        logger.error(f"Error in update_code_in_db for card {code_id}: {str(e)}", exc_info=True)
        raise e
    finally:
        conn.close()
