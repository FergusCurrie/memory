import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

CSV_DIR = "/workspaces/memory/memory_backups/memory_datasets/data"
import pandas as pd

# SQL Server connection URL format
conn_url = "mssql+pyodbc://sa:32rsrg5ty3t%gst42@tsql_db:1433/memory?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"

engine = create_engine(conn_url)
session = Session(engine)

from sqlalchemy import text


def list_tables():
    # Query to get all tables and their schemas
    query = text("""
        SELECT 
            t.name AS TableName,
            s.name AS SchemaName
        FROM 
            sys.tables t
        INNER JOIN 
            sys.schemas s ON t.schema_id = s.schema_id
        ORDER BY 
            s.name, t.name;
    """)

    result = session.execute(query)

    print("Tables in the database:")
    for row in result:
        print(f"Schema: {row.SchemaName}, Table: {row.TableName}")


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
            chunksize=100,
        )
        print("sent to db")

        # Verify the data was copied
        # with engine.connect() as conn:
        #     result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        #     print(f"Rows copied to {table_name}: {result.scalar()}")

        # Create a record in Database

        # Create the dataset table if it doesn't exist
        # Base.metadata.create_all(engine)

        # Create and add the dataset record - this isn't done her... this is only for postgres
        # new_dataset = Dataset(name=table_name)
        # session.add(new_dataset)
        # session.commit()
        # session.refresh(new_dataset)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_tables()

    if len(sys.argv) > 1 and sys.argv[1] == "add":
        add_datasets()
