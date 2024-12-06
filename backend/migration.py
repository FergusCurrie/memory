from backend.models import Code
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Use the same connection URL as in your models.py
# conn_url = "mssql+pyodbc://sa:32rsrg5ty3t%gst42@tsql_db:1433/memory?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
conn_url = "postgresql+psycopg2://ferg234e1341:32rsrg5ty3t%gst42@postgres_db/memory_db"
engine = create_engine(conn_url)


def migrate():
    with Session(engine) as session:
        # Update existing records
        session.query(Code).filter(Code.type == None).update({"type": "polars"})

        session.commit()
        print("Migration completed successfully")


if __name__ == "__main__":
    migrate()
