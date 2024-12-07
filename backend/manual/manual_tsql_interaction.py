import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

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

CSV_DIR = "/workspaces/memory/memory_backups/memory_datasets/data"
import pandas as pd

# SQL Server connection URL format
conn_url = "mssql+pyodbc://sa:32rsrg5ty3t%gst42@tsql_db:1433/memory?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
from backend.dbs.tsql_connection import get_tsql_conn

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


def book():
    print("Adding book data to TSQL database")

    # Get SQL file contents
    sql_file_path = "manual/temp_data_old_db/tsql_book.sql"
    with open(sql_file_path, "r") as file:
        sql_commands = file.read()

    # Split into individual commands on GO statements
    commands = sql_commands.split("GO")

    # Connect to database
    # conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={config['tsql_server']};DATABASE={config['tsql_database']};UID={config['tsql_user']};PWD={config['tsql_password']};TrustServerCertificate=yes"
    # conn = pyodbc.connect(get_tsql_conn())
    # cursor = conn.cursor()
    print("check")
    print(len(commands))

    engine = create_engine(get_tsql_conn())
    with engine.connect() as conn:
        with conn.begin():
            for command in commands:
                # print(command)
                conn.execute(text(command))
    #     result = conn.execute(text(self._add_schema(code)))
    # # Execute each command
    # for command in commands:
    #     if command.strip():
    #         try:
    #             cursor.execute(command)
    #             conn.commit()
    #         except Exception as e:
    #             print(f"Error executing command: {e}")
    #             print(f"Failed command was: {command[:100]}...")  # Print first 100 chars of failed command
    #             conn.rollback()

    # cursor.close()
    # conn.close()
    # print("Finished adding book data")


def read_sql_book_to_csv():
    """Read all tables from TSQL book database and save to CSV files"""
    import os
    import pandas as pd
    from backend.dbs.tsql_connection import get_tsql_conn
    from sqlalchemy import create_engine

    # Create output directory if it doesn't exist
    output_dir = "manual/temp_data_old_db/tsql_book"
    os.makedirs(output_dir, exist_ok=True)

    # Get list of all tables
    engine = create_engine(get_tsql_conn())

    # Export each table to CSV
    for table in tables_sql_book:
        print(f"Exporting {table}")
        with engine.connect() as conn:
            # Read table into pandas DataFrame
            df = pd.read_sql(f"SELECT * FROM dbo.{table}", conn)

            # Save to CSV
            output_file = os.path.join(output_dir, f"{table}.csv")
            df.to_csv(output_file, index=False)
            print(f"Saved {output_file}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_tables()

    if len(sys.argv) > 1 and sys.argv[1] == "add":
        add_datasets()

    if len(sys.argv) > 1 and sys.argv[1] == "book":
        book()

    if len(sys.argv) > 1 and sys.argv[1] == "dump":
        read_sql_book_to_csv()
