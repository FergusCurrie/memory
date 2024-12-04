import pyodbc 

import pandas as pd
import polars as pl
import pyodbc

def sql_server_query(query):
    server = 'sqledge'  # This is the name of your Azure SQL Edge container
    database = 'datasets'
    username = 'sa'
    password = 'bigStrfefongPwd4234#!#'

    conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;Encrypt=yes;'

    conn = pyodbc.connect(conn_str)
    
    # Execute the query and fetch the results into a pandas DataFrame
    df = pl.DataFrame(pd.read_sql(query, conn))

    # Close the connection
    conn.close()

    return df
