import io
import logging
import pandas as pd
import polars as pl
from contextlib import redirect_stderr, redirect_stdout

logger = logging.getLogger(__name__)


def run_code(code, dataset_path):
    df = pl.read_csv(dataset_path)

    # Capture stdout and stderr
    output = io.StringIO()
    error = io.StringIO()

    with redirect_stdout(output), redirect_stderr(error):
        local_vars = {"df": df}
        exec("import polars as pl\n" + code, {}, local_vars)
    if "result" in local_vars:
        return pd.DataFrame(local_vars["result"].to_dict())

    return pd.DataFrame()


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
    description = code_completion_row["description"]
    dataset_path = code_completion_row["dataset_path"]
    target = pd.read_json(str(code_completion_row["resulting_dataframe"]))
    code_text = code_submission.code
    logger.info(code_text)
    executed_df = run_code(code_text, dataset_path)

    logger.info(target)
    logger.info(executed_df)

    # Test result
    if compare_dataframes(executed_df, target):
        return True, executed_df.head(10).to_json()
    return False, executed_df.head(10).to_json()
