from backend.crud import add_code_to_problem, create_problem
from sqlalchemy import create_engine, select, text

conn_url = "postgresql+psycopg2://ferg234e1341:32rsrg5ty3t%gst42@postgres_db/memory_db"

engine = create_engine(conn_url)
from sqlalchemy.orm import Session

session = Session(engine)


def check():
    for tbl in ["dataset", "problem", "code", "review"]:
        print(tbl + ":")
        stmt = select("*").select_from(text(tbl))
        result = session.execute(stmt)
        rows = result.fetchall()
        for row in rows:
            print(row)


def add():
    prob = create_problem(session, "Simple example problem")
    add_code_to_problem(session, "result = (academic)", "academic", prob.id)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check()
    if len(sys.argv) > 1 and sys.argv[1] == "add":
        add()


# from sqlalchemy import create_engine

# conn_url = "postgresql+psycopg2://ferg234e1341:32rsrg5ty3t%gst42@postgres_db/memory_db"

# engine = create_engine(conn_url)
# from sqlalchemy.orm import Session

# session = Session(engine)

# import pandas as pd
# from sqlalchemy import text

# # Read CSV file into DataFrame
# df = pd.read_csv("memory_backups/academic.csv")

# # Copy DataFrame to PostgreSQL using to_sql()
# table_name = "academic"
# df.to_sql(
#     name=table_name,
#     con=engine,
#     if_exists="replace",  # or 'append'
#     index=False,
#     method="multi",
# )

# # Verify the data was copied
# with engine.connect() as conn:
#     result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
#     print(f"Rows copied to {table_name}: {result.scalar()}")

# # Create a record in Database
# from backend.models import Dataset

# # Create the dataset table if it doesn't exist
# # Base.metadata.create_all(engine)

# # Create and add the dataset record
# new_dataset = Dataset(name="academic")
# session.add(new_dataset)
# session.commit()
# session.refresh(new_dataset)

# # Verify the dataset was added
# result = session.query(Dataset).filter(Dataset.name == "academic").first()
# if result:
#     print(f"Dataset '{result.name}' successfully added with id {result.id}")
# else:
#     print("Failed to add dataset")
