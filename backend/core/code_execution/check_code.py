import io
import logging
import pandas as pd
import polars as pl
from ..sqlserver.query import sql_server_query
from contextlib import redirect_stderr, redirect_stdout

logging.getLogger("py4j").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

DATA_PATH = "backend/code_execution/data/"


def _clean_result_to_pandas(result):
    # Convert result to DataFrame if it's a Series
    if isinstance(result, pl.Series):
        result = result.to_frame()
    result = result.to_dict()
    return pl.DataFrame(result)


def _execute_code(code, local_variables):
    logger.info(f"local vars = {local_variables}")
    output = io.StringIO()
    error = io.StringIO()
    try:
        with redirect_stdout(output), redirect_stderr(error):
            exec(code, {}, local_variables)
        if "result" in local_variables:
            return _clean_result_to_pandas(local_variables["result"]), None
        logger.info("raise exception")
        raise Exception("No result value found")
    except Exception as e:
        logger.info(f"Exception hit {e} {error}")
        error_output = error.getvalue().strip()
        if error_output:
            logger.info(error_output)
            return None, error_output
        return pl.DataFrame(), str(e)


def run_code_polars(code, datasets, preprocessing_code):
    """Execute code and return result

    Args:
        code (string): code to execute
        datasets (list[str]): list of csv datasets to load in
        preprocessing_code (string): any initial code to execute

    Returns:
        pd.DataFrame, str : Resulting dataframe and error (if error raised)
    """

    # Polish the input code, and necassary polars imports
    if preprocessing_code != "":
        code_to_run = f"import polars as pl\n{preprocessing_code}\n" + code
    else:
        code_to_run = "import polars as pl\n" + code

    # Execute and return
    result = _execute_code(code_to_run, datasets)
    logger.info(result)
    return result


def run_code_pyspark(code, datasets, preprocessing_code):
    logger.info("RUnning pyspark code")
    # Load datasets
    dfs = {}
    for dataset in datasets:
        x = pd.read_csv(DATA_PATH + dataset + ".csv")
        dfs[dataset.replace(".csv", "")] = x

    # Setup pyspark code
    pyspark_code = 'from pyspark.sql import SparkSession\nspark = SparkSession.builder.appName("LocalSparkExample").master("local[*]").getOrCreate()\n'

    for df_name in dfs:
        pyspark_code += f"{df_name} = spark.createDataFrame({df_name})\n"
    pyspark_code += code
    pyspark_code += "\nresult = result.toPandas()\nspark.stop()"
    logger.info(pyspark_code)
    # Run and return
    result = _execute_code(pyspark_code, dfs)
    logger.info(result)
    return result


def run_code_sql(code, datasets, preprocessing_code):
    logger.info("Running sql code")
    df = sql_server_query(code)
    try:
        return df, None
    except Exception as e:
        logger.info(f"Exception hit {e}")
        return pl.DataFrame(), e


def run_code_to_check_results_for_card_creation(code, datasets, preprocessing_code, problem_type):
    if problem_type == "polars":
        check_function = run_code_polars
    elif problem_type == "pyspark":
        check_function = run_code_pyspark
    elif problem_type == "sql":
        check_function = run_code_sql
    else:
        raise Exception(f"Problem type {problem_type} not supported")

    return check_function(code, datasets, preprocessing_code)


def run_code_against_test(problem, code_submission):
    # Test the code
    # datasets = [x for x in list(problem["datasets"].keys()) if x != "preprocessing"]  # this is actually a list of paths
    datasets = problem["datasets"]
    preprocessing_code = problem["preprocessing_code"]
    solution_code = problem["code"]
    intput_code = code_submission.code

    problem_type = problem["type"]

    if problem_type == "polars":
        check_function = run_code_polars
    elif problem_type == "pyspark":
        check_function = run_code_pyspark
    elif problem_type == "sql":
        check_function = run_code_sql
    else:
        raise Exception(f"Problem type {problem_type} not supported")

    # Run solution and attempt
    submission_df, submission_error = check_function(intput_code, datasets, preprocessing_code)
    solution_df, solution_error = check_function(solution_code, datasets, preprocessing_code)

    logger.info(solution_df)
    logger.info(submission_df)

    # Test result
    # if compare_dataframes(submission_df, solution_df):
    #     return True, submission_df.head(10).to_json(), submission_error
    logger.info([c for c in solution_df.columns])
    # solution_df = solution_df.sort([c for c in solution_df.columns])
    # submission_df = solution_df.sort([c for c in solution_df.columns])
    if solution_df.equals(submission_df):
        return True, submission_df.to_pandas().head(10).to_json(), submission_error
    return False, submission_df.to_pandas().head(10).to_json(), submission_error
