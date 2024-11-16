from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

conn_url = "postgresql+psycopg2://ferg234e1341:32rsrg5ty3t%gst42@postgres_db/memory_db"

engine = create_engine(conn_url)

db = scoped_session(sessionmaker(bind=engine))

query_rows = db.execute(text("SELECT table_name FROM information_schema.tables"))

for register in query_rows:
    print(register)
# query_rows = db.execute("SELECT * FROM anyTableName").fetchall()
# for register in query_rows:
#     print(f"{register.col_1_name}, {register.col_2_name}, ..., {register.col_n_name}")
#     # Note that this Python way of printing is available in Python3 or more!!
