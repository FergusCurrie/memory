from backend.core.scheduling.Scheduler import Scheduler
from backend.crud import create_due_date, get_all_problems, get_reviews_for_problem
from backend.dbs.postgres_connection import get_postgres_conn
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

CSV_DIR = "/workspaces/memory/memory_backups/memory_datasets/data"
CSV_DIR = "manual/temp_data_old_db/tsql_book/"

conn_url = get_postgres_conn()

engine = create_engine(conn_url)

session = Session(engine)
scheduler = Scheduler()
for problem in get_all_problems(session):
    try:
        reviews = get_reviews_for_problem(session, problem.id)
        due = scheduler.get_next_review_date(problem, reviews)
        print(type(due))
        create_due_date(session, problem.id, due, "sm2")
    except:
        print(problem.description)
