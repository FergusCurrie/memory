import sqlite3
from backend.config import DB_PATH


# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Notes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tags JSON DEFAULT '{}',
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create Review table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note_id INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        result BOOLEAN,
        FOREIGN KEY (note_id) REFERENCES notes (id)
    )
    """)

    # Create Card table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note_id INTEGER,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        FOREIGN KEY (note_id) REFERENCES notes (id)
    )
    """)

    # Create Code Completion table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS code_completion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note_id INTEGER,
        dataframe_header JSON,
        solution_dataframe JSON,
        problem_description TEXT,
        dataset_path TEXT,
        FOREIGN KEY (note_id) REFERENCES notes (id)           
    )
    """)

    conn.commit()
    conn.close()


init_db()
