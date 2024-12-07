from backend.load_env_config import get_env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = get_env()


def get_postgres_conn():
    postgres_user = config["postgres_user"]
    postgres_password = config["postgres_password"]
    postgres_server = config["postgres_server"]
    postgres_db = config["postgres_db"]

    conn_url = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_server}/{postgres_db}"

    return conn_url


# Add this dependency
def get_postgres_db():
    conn_url = get_postgres_conn()
    engine = create_engine(conn_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
