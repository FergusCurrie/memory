import os
import pandas as pd
from backend.crud import add_code_to_problem, create_problem, delete_dataset
from backend.dbs.postgres_connection import get_postgres_conn
from backend.models import Buried
from sqlalchemy import create_engine, delete, select, text
from sqlalchemy.orm import Session

CSV_DIR = "/workspaces/memory/memory_backups/memory_datasets/data"
CSV_DIR = "manual/temp_data_old_db/tsql_book/"

conn_url = get_postgres_conn()

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
            name=table_name.lower(),
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
        new_dataset = Dataset(name=table_name.lower())
        session.add(new_dataset)
        session.commit()
        session.refresh(new_dataset)

        # Verify the dataset was added
        # result = session.query(Dataset).filter(Dataset.name == table_name).first()
        # if result:
        #     print(f"Dataset '{result.name}' successfully added with id {result.id}")
        # else:
        #     print("Failed to add dataset")


def schema():
    # Query to get all tables in postgres db
    query = text("""
        SELECT 
            tablename 
        FROM 
            pg_catalog.pg_tables
        WHERE 
            schemaname != 'pg_catalog' 
            AND schemaname != 'information_schema';
    """)

    result = session.execute(query)

    print("Tables in PostgreSQL database:")
    for row in result:
        print(row.tablename)


def check():
    for tbl in ["due"]:
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


def delete_col_table():
    session.execute(text("ALTER TABLE code DROP COLUMN type"))
    session.commit()
    session.execute(text("ALTER TABLE code DROP COLUMN default_code"))
    session.commit()
    print("Column 'type' , 'default_code'  dropped from Code table")


def delete_table():
    conn_url = get_postgres_conn()

    engine = create_engine(conn_url)

    session = Session(engine)
    session.execute(text("DROP TABLE IF EXISTS due CASCADE"))
    session.commit()
    return
    tables_sql_book = [
        "Categories",
        "Customers",
        "Employees",
        "Nums",
        "OrderDetails",
        "Orders",
        "Products",
        "Scores",
        "Shippers",
        "Suppliers",
        "Tests",
    ]

    for tbl in tables_sql_book:
        print(f"DROP TABLE IF EXISTS {tbl}")
        session.execute(text(f"DROP TABLE IF EXISTS {tbl} CASCADE"))
        session.commit()
        delete_dataset(session, tbl)
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

    if len(sys.argv) > 1 and sys.argv[1] == "delete_col":
        delete_col_table()

    if len(sys.argv) > 1 and sys.argv[1] == "schema":
        schema()
