from backend.load_env_config import get_env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = get_env()

# Connection parameters
server = config["tsql_server"]
user = config["tsql_user"]
password = config["tsql_password"]
database = config["tsql_database"]

# Create connection string
conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password};TrustServerCertificate=yes"

# Replace the raw connection URL with a more secure configuration
engine = create_engine(conn_str)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Add this dependency
def get_tsql_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
