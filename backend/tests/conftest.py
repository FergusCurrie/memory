import os
import pytest
import sys

print("\nPython executable:", sys.executable)
print("Python path:", sys.path)
print("Current working directory:", os.getcwd())
from backend.models import Base  # Import your Base from your main app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="function")
def test_db():
    # Create an in-memory SQLite database for testing
    # engine = create_engine(
    #     "postgresql+psycopg2://ferg234e1341:32rsrg5ty3t%gst42@postgres_db/memory_db"
    # )
    engine = create_engine("sqlite:///memory:?cache=shared")
    # Create all tables
    Base.metadata.create_all(engine)

    # Create a new session factory
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create a new session for the test
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)
