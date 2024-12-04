import logging
import polars as pl
from backend.models import Code, Dataset, Problem
from sqlalchemy import select, text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def create_problem(session: Session, description: str) -> Problem:
    new_problem = Problem(description=description)
    session.add(new_problem)
    session.commit()
    session.refresh(new_problem)
    return new_problem


def create_dataset(session: Session, name: str) -> Problem:
    new_dataset = Dataset(name=name)
    session.add(new_dataset)
    session.commit()
    session.refresh(new_dataset)
    return new_dataset


def add_code_to_problem(session: Session, code_table_name: str, problem_id: int):
    new_code = Code(code_table_name=code_table_name, problem_id=problem_id)
    session.add(new_code)
    session.commit()
    session.refresh(new_code)
    return new_code


def get_problem(session: Session, problem_id: int) -> dict:
    problem = session.query(Problem).filter(Problem.id == problem_id).first()
    codes = session.query(Code).filter(Code.problem_id == problem_id).all()
    code_table_names = [code.code_table_name for code in codes] if codes else []

    return {
        "id": problem.id,
        "description": problem.description,
        "date_created": problem.date_created,
        **({"code_table_names": code_table_names} if code_table_names else {}),
    }


def get_dataset(session: Session, table_name: str) -> pl.DataFrame:
    stmt = select("*").select_from(text(table_name))
    result = session.execute(stmt)
    rows = result.fetchall()
    # Get column names from first row
    columns = result.keys()
    # Convert rows to list of dictionaries
    data = [dict(zip(columns, row)) for row in rows]
    # Create polars dataframe from dictionaries
    df = pl.DataFrame(data)
    return df
    for row in rows:
        print(row)


def list_available_datasets(session: Session):
    # Query all unique code table names from the Code model
    stmt = select(Dataset.name).distinct()
    result = session.execute(stmt)
    unique_datasets = result.scalars().all()

    # Log the actual results for debugging
    logger.info(f"Found datasets: {unique_datasets}")

    # Return empty list if no datasets found
    if not unique_datasets:
        logger.info("No datasets found in database")
        return []

    return unique_datasets
