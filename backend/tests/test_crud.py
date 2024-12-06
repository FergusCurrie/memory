import polars as pl
from ..core.scheduling.Scheduler import Scheduler
from backend.crud import (
    add_code_to_problem,
    create_dataset,
    create_problem,
    create_review,
    get_all_problems,
    get_code_for_problem,
    get_dataframes_for_problem,
    get_dataset,
    get_list_of_datasets_for_problem,
    get_problem,
    get_reviews_for_problem,
    list_available_datasets,
)
from datetime import datetime, timedelta


def test_create_problem(test_db):
    description = "test description"
    problem = create_problem(test_db, description)
    assert problem.description == "test description"


def test_create_simple_problem(test_db):
    description = "test description"
    problem = create_problem(test_db, description)
    code = add_code_to_problem(test_db, "", "academic", problem.id)
    assert code.datasets == "academic"


def test_get_problem_1(test_db):
    description = "test description"
    problem = create_problem(test_db, description)
    code = add_code_to_problem(test_db, "", "academic", problem.id)
    assert code.datasets == "academic"

    # Now try query get_problem
    p = get_problem(test_db, problem.id).to_dict()
    assert p["description"] == description


def test_get_code(test_db):
    description = "test description"
    problem = create_problem(test_db, description)
    code_create = add_code_to_problem(test_db, "", "academic", problem.id)
    code = get_code_for_problem(test_db, problem.id)
    assert code_create.to_dict() == code[0].to_dict()


def test_get_example_dataset(test_db):
    df = pl.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    # Convert polars DataFrame to pandas DataFrame and add to test database
    pandas_df = df.to_pandas()
    pandas_df.to_sql(name="test_table", con=test_db.bind, if_exists="replace", index=False)

    result_df = get_dataset(test_db, "test_table")

    assert result_df.equals(df)


def test_get_available_datasets(test_db):
    dataset = create_dataset(test_db, name="academic")
    assert list_available_datasets(test_db) == ["academic"]


def test_create_simple_code_problem(test_db):
    dataset = create_dataset(test_db, name="academic")
    new_prob = create_problem(test_db, "testing")
    code = """
    result = (
        academic
    )
    """
    add_code_to_problem(session=test_db, code=code, datasets="academic", problem_id=new_prob.id)
    assert 1 == 1


def test_create_review(test_db):
    new_prob = create_problem(test_db, "testing")
    new_review = create_review(test_db, new_prob.id, 1)
    assert new_review.result == 1


def test_get_review(test_db):
    new_prob = create_problem(test_db, "testing")
    new_review = create_review(test_db, new_prob.id, 1)
    review = get_reviews_for_problem(test_db, new_prob.id)[0].to_dict()
    assert review["date_created"] == datetime.now().date()
    assert review["id"] == 1
    assert review["problem_id"] == 1
    assert review["result"] == 1


def test_schedule_card_no_reviews(test_db):
    create_date = datetime.now() - timedelta(days=7)
    new_prob = create_problem(test_db, "testing", date_created=create_date)
    scheduler = Scheduler()
    assert scheduler.check_problem_ready_for_review(new_prob, [])


def test_schedule_card_one_review(test_db):
    new_prob = create_problem(test_db, "testing")
    new_review = create_review(test_db, new_prob.id, 1)
    scheduler = Scheduler()
    assert not scheduler.check_problem_ready_for_review(new_prob, [new_review])


def test_study_problem(test_db):
    """
    Studying a problem requires:
    - Fetching all problem ids
    - Fetching associated reviews
    - Determining which are ready for review
    - For those ready to review, fetching all characteristics
    """
    description = "test description"
    problem = create_problem(test_db, description)
    code = add_code_to_problem(test_db, "", "academic", problem.id)
    assert code.datasets == "academic"


def test_get_all_problems(test_db):
    problem1 = create_problem(test_db, "1")
    problem2 = create_problem(test_db, "2")
    problem3 = create_problem(test_db, "3")

    probs = get_all_problems(test_db)
    assert [p.description for p in probs] == ["1", "2", "3"]


def test_get_tables_from_problem(test_db):
    """
    Adds a dataset to db.
    Creates new problem, adds code and dataset.
    Queries the dataframe associated to problem
    Asserts they're equal.
    """
    # Add dataset
    df = pl.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    # Convert polars DataFrame to pandas DataFrame and add to test database
    pandas_df = df.to_pandas()
    pandas_df.to_sql(name="academic", con=test_db.bind, if_exists="replace", index=False)

    dataset = create_dataset(test_db, name="academic")
    new_prob = create_problem(test_db, "testing")
    code = """
    result = (
        academic
    )
    """
    add_code_to_problem(session=test_db, code=code, datasets="academic", problem_id=new_prob.id)

    tables = get_list_of_datasets_for_problem(test_db, new_prob.id)
    assert tables == ["academic"]

    frames = get_dataframes_for_problem(test_db, new_prob.id)
    assert frames["academic"].equals(df)
