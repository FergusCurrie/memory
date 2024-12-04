import pandas as pd 
import polars as pl 
import pyodbc

server = 'sqledge'  # This is the name of your Azure SQL Edge container
database = 'datasets'
username = 'sa'
password = 'bigStrfefongPwd4234#!#'

def get_sql_type(dtype):
    if dtype == pl.String:
        return 'NVARCHAR(MAX)'
    elif dtype == pl.Int64:
        return 'BIGINT'
    elif dtype == pl.Float64:
        return 'FLOAT'
    elif dtype == pl.Boolean:
        return 'BIT'
    elif dtype == pl.Datetime:
        return 'DATETIME2'
    else:
        return 'NVARCHAR(MAX)'  # Default to NVARCHAR(MAX) for unknown types


def add_table_from_csv(csv):
    """
    Passed a csv file name. Loads it into sql server.
    """
    df = pl.read_csv(f"backend/code_execution/data/{csv}")

    columns = ["id INT IDENTITY(1,1) PRIMARY KEY"]
    for column, dtype in zip(df.columns, df.dtypes):
        sql_type = get_sql_type(dtype)
        columns.append(f"[{column}] {sql_type}")

    create_table_query = f"""
    CREATE TABLE {csv.replace('.csv','')} (
        {', '.join(columns)}
    )
    """

    conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;Encrypt=yes;'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()

    for row in df.iter_rows():
        placeholders = ', '.join(['?' for _ in row])
        insert_query = f"""
        INSERT INTO {csv.replace('.csv','')} ({', '.join([f'[{col}]' for col in df.columns])})
        VALUES ({placeholders})
        """
        cursor.execute(insert_query, *row)
    conn.commit()
    cursor.close()
    conn.close()

