import logging
import polars as pl
from backend.models import Buried, Code, Dataset, Problem, Review, Suspended
from datetime import datetime
from sqlalchemy import select, text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def create_problem(session: Session, description: str, date_created: datetime = None) -> Problem:
    if date_created is None:
        new_problem = Problem(description=description)
    else:
        new_problem = Problem(description=description, date_created=date_created)
    session.add(new_problem)
    session.commit()
    session.refresh(new_problem)
    return new_problem


def update_problem(session: Session, problem_id: int, description_new: str) -> Problem:
    problem = session.query(Problem).filter(Problem.id == problem_id).first()
    if problem is None:
        raise Exception("probloem should not be none ")
        return None
    problem.description = description_new
    session.commit()
    session.refresh(problem)
    return problem


def toggle_suspend(session: Session, problem_id: int) -> Suspended:
    suspended = session.query(Suspended).filter(Suspended.problem_id == problem_id).all()

    # If no suspended record, create suspending record
    if suspended == []:
        value = True
    else:
        suspended.sort(key=lambda x: x.date_created, reverse=True)
        value = not suspended[0].is_suspended
    s = Suspended(is_suspended=value, problem_id=problem_id)
    session.add(s)
    session.commit()
    session.refresh(s)
    return s


def create_review(session, problem_id: int, result: int, date_created: datetime = None):
    result_int = 1 if result else 0
    if date_created is None:
        new_review = Review(problem_id=problem_id, result=result_int)
    else:
        new_review = Review(problem_id=problem_id, result=result_int, date_created=date_created)
    session.add(new_review)
    session.commit()
    session.refresh(new_review)
    return new_review


def get_reviews_for_problem(session, problem_id: int):
    reviews = session.query(Review).filter(Review.problem_id == problem_id).all()
    return reviews


def create_dataset(session: Session, name: str) -> Problem:
    # Check if dataset already exists
    existing_dataset = session.query(Dataset).filter(Dataset.name == name).first()
    if existing_dataset is not None:
        logger.info(f"Dataset already exists {name}")
        return existing_dataset

    new_dataset = Dataset(name=name)
    session.add(new_dataset)
    session.commit()
    session.refresh(new_dataset)
    return new_dataset


def add_code_to_problem(session: Session, code: str, datasets: str, problem_id: int, type: str, default_code: str):
    new_code = Code(code=code, datasets=datasets, problem_id=problem_id, type=type, default_code=default_code)
    session.add(new_code)
    session.commit()
    session.refresh(new_code)
    return new_code


def update_code(session: Session, code: str, datasets: str, problem_id: int, default_code: str):
    code_obj = session.query(Code).filter(Code.problem_id == problem_id).first()
    if code_obj is None:
        return None
    if code is not None:
        code_obj.code = code
    if datasets is not None:
        code_obj.datasets = datasets
    if default_code is not None:
        code_obj.default_code = default_code
    session.commit()
    session.refresh(code_obj)
    return code_obj


# def get_problem(session: Session, problem_id: int) -> dict:
#     problem = session.query(Problem).filter(Problem.id == problem_id).first()
#     codes = session.query(Code).filter(Code.problem_id == problem_id).all()
#     code_table_names = [code.datasets for code in codes] if codes else []

#     return {
#         "id": problem.id,
#         "description": problem.description,
#         "date_created": problem.date_created,
#         **({"code_table_names": code_table_names} if code_table_names else {}),
#     }


def get_problem(session: Session, problem_id: int) -> dict:
    problem = session.query(Problem).filter(Problem.id == problem_id).all()
    if len(problem) > 1:
        raise Exception("Should only be one match for problem")
    return problem[0]


def get_code_for_problem(session: Session, problem_id: int):
    return session.query(Code).filter(Code.problem_id == problem_id).all()


def get_list_of_datasets_for_problem(session: Session, problem_id: int):
    codes = session.query(Code).filter(Code.problem_id == problem_id).all()
    if not codes:
        return []
    # Split the comma-separated dataset names and flatten the list
    datasets = [dataset.strip() for code in codes for dataset in code.datasets.split(",") if dataset.strip()]
    return datasets


def get_dataframes_for_problem(session: Session, problem_id: int):
    datasets = get_list_of_datasets_for_problem(session, problem_id)
    return {d: get_dataset(session, d) for d in datasets}


def get_dataset(session: Session, table_name: str) -> pl.DataFrame:
    stmt = select("*").select_from(text(table_name))
    result = session.execute(stmt)
    rows = result.fetchall()
    columns = result.keys()
    data = [dict(zip(columns, row)) for row in rows]
    return pl.DataFrame(data)


def list_available_datasets(session: Session):
    stmt = select(Dataset.name).distinct()
    result = session.execute(stmt)
    return result.scalars().all()


def get_all_problems(session: Session):
    return session.query(Problem).all()


def toggle_suspend(session: Session, problem_id: int) -> Suspended:
    suspended = session.query(Suspended).filter(Suspended.problem_id == problem_id).all()
    value = len(suspended) % 2 != 0
    s = Suspended(is_suspended=value, problem_id=problem_id)
    session.add(s)
    session.commit()
    session.refresh(s)
    return s


def bury_problem(session: Session, problem_id: int, date_created: datetime = None) -> Buried:
    b = Buried(problem_id=problem_id, date_created=date_created)
    session.add(b)
    session.commit()
    session.refresh(b)
    return b


def check_problem_suspended(session: Session, problem_id: int) -> bool:
    suspended = session.query(Suspended).filter(Suspended.problem_id == problem_id).all()
    return len(suspended) % 2 != 0


def check_problem_buried(session: Session, problem_id: int) -> bool:
    buried = session.query(Buried).filter(Buried.problem_id == problem_id).all()
    if len(buried) == 0:
        return False
    return any(b.date_created == datetime.now().date() for b in buried)


# def get_all_non_suspended_problems(session: Session):
#     problems = session.query(Problem).all()
#     suspended = session.query(Suspended).all()
#     suspended_dict = {}
#     for s in suspended:
#         if s.problem_id not in suspended_dict or s.date_created > suspended_dict[s.problem_id][1]:
#             suspended_dict[s.problem_id] = (s.is_suspended, s.date_created)

#     return [p for p in problems if p.id not in suspended_dict or not suspended_dict[p.id][0]]


def get_all_reviews(session: Session):
    return session.query(Review).all()
