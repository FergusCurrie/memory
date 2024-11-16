# Azure sql on mac

https://database.guide/how-to-install-sql-server-on-an-m1-mac-arm64/
docker pull mcr.microsoft.com/azure-sql-edge
docker run --cap-add SYS_PTRACE -e 'ACCEPT_EULA=1' -e 'MSSQL_SA_PASSWORD=bigStrfefongPwd4234#!#' --network memory-network -p 1433:1433 --name sqledge -d mcr.microsoft.com/azure-sql-edge

Need to create a docker network for devctonainer, deployment, and sql edge to be able to hit each othe:

```
docker network create memory-network
```

Setup a database

`CREATE DATABASE datasets;`

Setup a table

Basic query example:

```
import pyodbc

server = 'sqledge'  # This is the name of your Azure SQL Edge container
database = 'master'
username = 'sa'
password = 'bigStrfefongPwd4234#!#'

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;Encrypt=yes;'

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

query = """
SELECT
    t.name AS TableName,
    s.name AS SchemaName
FROM
    sys.tables t
INNER JOIN
    sys.schemas s ON t.schema_id = s.schema_id
ORDER BY
    s.name, t.name;
"""
cursor.execute(query)

# Fetch all results
tables = cursor.fetchall()

# Print the results
print("Tables in the database:")
for table in tables:
    print(f"Schema: {table.SchemaName}, Table: {table.TableName}")

# Close the cursor and connection
cursor.close()
conn.close()
```

# Fixing

```
ERROR in ./src/App.tsx 13:0-36
Module not found: Error: Can't resolve './pages/Browse' in '/workspaces/memory/frontend/src'
resolve './pages/Browse' in '/workspaces/memory/frontend/src'
  using description file: /workspaces/memory/frontend/package.json (relative path: ./src)
    Field 'browser' doesn't contain a valid alias configuration
    using description file: /workspaces/memory/frontend/package.json (relative path: ./src/pages/Browse)
      no extension
        Field 'browser' doesn't contain a valid alias configuration
        /workspaces/memory/frontend/src/pages/Browse doesn't exist
      .ts
        Field 'browser' doesn't contain a valid alias configuration
        /workspaces/memory/frontend/src/pages/Browse.ts doesn't exist
      .tsx
        Field 'browser' doesn't contain a valid alias configuration
        /workspaces/memory/frontend/src/pages/Browse.tsx doesn't exist

```

Fix by:

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
source ~/.bashrc
nvm --version
nvm install -lts
nvm use --lts
```

## Readings

- https://github.com/zhanymkanov/fastapi-best-practices
