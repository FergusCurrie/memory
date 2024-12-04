from sqlalchemy import create_engine, select, text

conn_url = "postgresql+psycopg2://ferg234e1341:32rsrg5ty3t%gst42@postgres_db/memory_db"

engine = create_engine(conn_url)
from sqlalchemy.orm import Session

session = Session(engine)

stmt = select("*").select_from(text("dataset"))
result = session.execute(stmt)
rows = result.fetchall()
for row in rows:
    print(row)
