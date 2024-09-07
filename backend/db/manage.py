import sqlite3


# Initialize the database
def init_db():
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()

    # Create Card table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create Review table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_id INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        result BOOLEAN,
        FOREIGN KEY (card_id) REFERENCES cards (id)
    )
    """)

    conn.commit()
    conn.close()


init_db()
