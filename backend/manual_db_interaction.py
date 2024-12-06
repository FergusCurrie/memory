import os
import pandas as pd
from backend.crud import add_code_to_problem, create_problem
from backend.models import Buried
from sqlalchemy import create_engine, delete, select, text
from sqlalchemy.orm import Session

CSV_DIR = "/workspaces/memory/memory_backups/memory_datasets/data"

conn_url = "postgresql+psycopg2://ferg234e1341:32rsrg5ty3t%gst42@postgres_db/memory_db"

engine = create_engine(conn_url)

session = Session(engine)


def add_datasets():
    print("running add dbs")
    csvs = []
    for file in os.listdir(CSV_DIR):
        print(file)
        if ".csv" in file:
            csvs.append(file)
    print(csvs)
    # Read CSV file into DataFrame
    for csv in csvs:
        df = pd.read_csv(f"{CSV_DIR}/{csv}")
        # .head(10000)
        print(df.shape)
        df = df.head(1000)
        print(csv)
        # Copy DataFrame to PostgreSQL using to_sql()
        table_name = csv.replace(".csv", "")
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",  # or 'append'
            index=False,
            method="multi",
        )
        print("sent to db")

        # Verify the data was copied
        # with engine.connect() as conn:
        #     result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        #     print(f"Rows copied to {table_name}: {result.scalar()}")

        # Create a record in Database
        from backend.models import Dataset

        # Create the dataset table if it doesn't exist
        # Base.metadata.create_all(engine)

        # Create and add the dataset record
        new_dataset = Dataset(name=table_name)
        session.add(new_dataset)
        session.commit()
        session.refresh(new_dataset)

        # Verify the dataset was added
        # result = session.query(Dataset).filter(Dataset.name == table_name).first()
        # if result:
        #     print(f"Dataset '{result.name}' successfully added with id {result.id}")
        # else:
        #     print("Failed to add dataset")


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


def delete_rows_table():
    session.execute(delete(Buried))
    session.commit()
    print("dted")


def delete_table():
    session.execute(text("DROP TABLE IF EXISTS buried"))
    session.commit()
    print("Table dropped")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check()
    if len(sys.argv) > 1 and sys.argv[1] == "add":
        add()

    if len(sys.argv) > 1 and sys.argv[1] == "data":
        add_datasets()

    if len(sys.argv) > 1 and sys.argv[1] == "delete_rows":
        delete_rows_table()

    if len(sys.argv) > 1 and sys.argv[1] == "delete":
        delete_table()
