import pyodbc

# Connection parameters
server = "tsql_db"
user = "sa"
password = "32rsrg5ty3t%gst42"
database = "master"  # Connect to master first to create new database

# Create connection string
conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password};TrustServerCertificate=yes"


try:
    # Establish connection
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # First check if database exists
    cursor.execute("SELECT name FROM sys.databases WHERE name = 'memory'")
    exists = cursor.fetchone() is not None

    if not exists:
        # Set autocommit to True before creating database
        conn.autocommit = True
        cursor.execute("CREATE DATABASE memory")
        print("Database 'memory' created successfully")
    else:
        print("Database 'memory' already exists")

except pyodbc.Error as e:
    print(f"Error: {str(e)}")

finally:
    # Close connections
    if "cursor" in locals():
        cursor.close()
    if "conn" in locals():
        conn.close()
