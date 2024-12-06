from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace the raw connection URL with a more secure configuration
conn_url = "postgresql+psycopg2://ferg234e1341:32rsrg5ty3t%gst42@postgres_db/memory_db"
engine = create_engine(conn_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Add this dependency
def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
