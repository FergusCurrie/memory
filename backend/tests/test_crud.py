import polars as pl
from backend.crud import (
    add_code_to_problem,
    create_dataset,
    create_problem,
    get_dataset,
    get_problem,
    list_available_datasets,
)
from datetime import datetime


def test_create_problem(test_db):
    description = "test description"
    problem = create_problem(test_db, description)
    assert problem.description == "test description"


def test_create_simple_problem(test_db):
    description = "test description"
    problem = create_problem(test_db, description)
    code = add_code_to_problem(test_db, "academic", problem.id)
    assert code.code_table_name == "academic"


def test_get_problem_1(test_db):
    description = "test description"
    problem = create_problem(test_db, description)
    code = add_code_to_problem(test_db, "academic", problem.id)
    assert code.code_table_name == "academic"

    # Now try query get_problem
    p = get_problem(test_db, problem.id)
    assert p["description"] == description
    assert p["date_created"] == datetime.now().date()
    assert p["code_table_names"] == ["academic"]


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
