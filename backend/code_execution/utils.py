import io
import logging
import pandas as pd
import polars as pl
from contextlib import redirect_stderr, redirect_stdout

logger = logging.getLogger(__name__)

DATA_PATH = "backend/code_execution/data/"


def get_pandas_header(dataset_name):
    return str(pd.read_csv(DATA_PATH + dataset_name).head(3).to_json())


def get_preprocessing_headers(datasets, preprocessing_code):
    dfs = {}
    for dataset in datasets:
        dfs[dataset.replace(".csv", "")] = pl.read_csv(DATA_PATH + dataset)

    output = io.StringIO()
    error = io.StringIO()

    try:
        with redirect_stdout(output), redirect_stderr(error):
            local_vars = dfs
            exec(f"import polars as pl\n{preprocessing_code}\n", {}, local_vars)

        if "preprocessed" in local_vars:
            result = local_vars["preprocessed"]  # .to_dict()
            # Convert result to DataFrame if it's a Series
            if isinstance(result, pl.Series):
                result = result.to_frame()
            result = result.to_dict()
            return pd.DataFrame(result).head(3).to_json()
        return pd.DataFrame()
    except Exception as e:
        logger.info(f"Exception hit {e} {error}")
        error_output = error.getvalue().strip()
        if error_output:
            logger.info(error_output)
            return None
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
