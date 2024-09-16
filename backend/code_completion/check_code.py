import io
import logging
import pandas as pd
import polars as pl
from contextlib import redirect_stderr, redirect_stdout

logger = logging.getLogger(__name__)


def get_pandas_header(dataset_name):
    return str(pd.read_csv("backend/code_completion/data/" + dataset_name).head(3).to_json())


def run_code(code, dataset_path):
    df = pl.read_csv("backend/code_completion/data/" + dataset_path)

    output = io.StringIO()
    error = io.StringIO()

    try:
        with redirect_stdout(output), redirect_stderr(error):
            local_vars = {"df": df}
            exec("import polars as pl\n" + code, {}, local_vars)

        if "result" in local_vars:
            return pd.DataFrame(local_vars["result"].to_dict()), None
        return pd.DataFrame(), None
    except Exception as e:
        error_output = error.getvalue().strip()
        if error_output:
            return None, error_output
        return pd.DataFrame(), str(e)


def compare_dataframes(df1, df2):
    # Check if the dataframes have the same columns
    if set(df1.columns) != set(df2.columns):
        return False

    # Sort both dataframes by all columns to ensure consistent order
    df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
    df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)

    # Compare the sorted dataframes
    return df1_sorted.equals(df2_sorted)


def run_code_against_test(code_completion_row, code_submission):
    # Test the code
    description = code_completion_row["problem_description"]
    dataset_path = code_completion_row["dataset_name"]
    solution_code = code_completion_row["code"]
    code_text = code_submission.code
    logger.info(code_text)

    # Run solution and attempt
    submission_df, submission_error = run_code(code_text, dataset_path)
    solution_df, solution_error = run_code(solution_code, dataset_path)

    logger.info(solution_df)
    logger.info(submission_df)

    # Test result
    if compare_dataframes(submission_df, solution_df):
        return True, submission_df.head(10).to_json(), submission_error
    return False, submission_df.head(10).to_json(), submission_error
