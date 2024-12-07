from backend.load_env_config import get_env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = get_env()


def get_tsql_conn():
    server = config["tsql_server"]
    user = config["tsql_user"]
    password = config["tsql_password"]
    database = config["tsql_database"]
    # conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password};TrustServerCertificate=yes"
    conn_url = f"mssql+pyodbc://{user}:{password}@{server}:1433/{database}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    return conn_url


# Add this dependency
def get_tsql_db():
    conn_str = get_tsql_conn()
    engine = create_engine(conn_str)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
