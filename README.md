# Memory

This is a implementation of memory app. I've switched to using fastapi.

## Readings

- https://github.com/zhanymkanov/fastapi-best-practices

## Db structure

![Alt text](docs/db.png)

## UI

![Alt text](docs/ui.png)

## Making a card

- Select any number of datasets. For code entry they will be in env by default, under name of datasets bar .csv.
- Enter some default code which will be prepopulated in editor
- Add whatever preprocessing code to prepare another dataframe. this can only produce 1 dataframe, preprocessed
- Add main code. This must product a dataframe 'result'.

## Setting up DevContainer

This project supports development using Visual Studio Code's DevContainers. DevContainers provide a consistent, isolated development environment that can be easily shared across team members. Follow these steps to set up and use the DevContainer:

1. Prerequisites:

   - Install [Visual Studio Code](https://code.visualstudio.com/)
   - Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Install the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension in VS Code

2. Clone the repository:

   ```
   git clone https://github.com/your-repo/memory-slim.git
   cd memory-slim
   ```

3. Open the project in VS Code:

   ```
   code .
   ```

4. When prompted, click "Reopen in Container" or use the command palette (F1) and select "Remote-Containers: Reopen in Container".

5. VS Code will build the DevContainer (this may take a few minutes the first time) and open the project inside the container.

6. Once inside the container, you'll have access to all the necessary tools and dependencies to develop and run the project.

7. You can now run the backend and frontend as described in the "Running the Basic Server" section, but from within the DevContainer environment.

The DevContainer configuration is defined in the `.devcontainer/devcontainer.json` file. This setup ensures that all developers are working with the same environment, reducing "it works on my machine" issues and simplifying onboarding for new team members.

## Running the Basic Server

To run the basic server for development purposes, follow these steps:

1. Set up poetry environment

   ```
   poetry shell
   ```

2. Start the FastAPI server:

   ```
   python3 -m backend.db.manage # to create dev db if not already setup
   uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
   ```

3. Set up the frontend:

   ```
   cd frontend
   npm install
   ```

4. Start the frontend development server:

   ```
   npm run dev
   ```

5. Access the application:
   Open your web browser and navigate to `http://localhost:3000` (or the port specified by your frontend dev server).

The backend API will be available at `http://localhost:8000`, and the frontend development server will proxy API requests to this address.

## Production Build

To create a production build of the Memory Slim application, follow these steps:

1. Build the frontend:

   ```
   cd frontend
   npm install
   npm run build
   ```

   This will create a production-ready build of the React app in the `static/frontend` directory.

2. Install Python dependencies:

   ```
   pip install poetry
   poetry install
   ```

3. Export Python dependencies to requirements.txt:

   ```
   poetry export -f requirements.txt --output requirements.txt --without-hashes
   ```

4. Build the Docker image:

   ```
   sudo docker build -f Dockerfile -t memory-prd .
   ```

5. Run the Docker container:
   ```
   sudo docker run -d -p 9898:9898 -v ~/docker_data/memory_slim_db:/app/db memory-prd
   sudo docker run -p 9898:9898 -v ~/docker_data/memory_slim_db:/app/db memory-prd
   ```
   -d is to run in detached mode.
   -p is to map port 9898 to port 9898 on the host machine.
   -v is to map the db directory to the host machine.

The application will now be accessible at `http://localhost:9898`.

Note: Make sure you have Docker installed on your system before running the Docker commands.

For convenience, steps 3-4 are combined in the `scripts/build.sh` script. You can run it with:

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