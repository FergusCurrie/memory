import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Replace the raw connection URL with a more secure configuration
conn_url = os.getenv("POSTGRES_URL")
engine = create_engine(conn_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Add this dependency
def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
