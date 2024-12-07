import io
import logging
import polars as pl
from contextlib import redirect_stderr, redirect_stdout

logger = logging.getLogger(__name__)


class CheckPolarsCode:
    """The goal is to generate a nice interface here. It takes"""

    def __init__(self):
        pass

    def _compare_dataframes(self, df1, df2):
        if set(df1.columns) != set(df2.columns):
            return False
        df1_sorted = df1.sort(by=df1.columns)
        df2_sorted = df2.sort(by=df2.columns)
        return df1_sorted.equals(df2_sorted)

    def _clean_result(self, result):
        # Convert result to DataFrame if it's a Series
        if isinstance(result, pl.Series):
            result = result.to_frame()
        result = result.to_dict()
        return pl.DataFrame(result)

    def run_code(self, code, datasets) -> [pl.DataFrame, str]:
        code = f"import polars as pl\n{code}"
        output = io.StringIO()
        error = io.StringIO()
        try:
            with redirect_stdout(output), redirect_stderr(error):
                exec(code, {}, datasets)
            if "result" in datasets:
                return self._clean_result(datasets["result"]), None
            logger.info("Run code found no result")
            return None, "result not found in run"
        except Exception as e:
            logger.info(f"Exception hit {e} {error}")
            error_output = error.getvalue().strip()
            if error_output:
                logger.info(error_output)
                return None, error_output
            return pl.DataFrame(), str(e)

    def compare_code(self, correct_code: str, submission_code: str, datasets: dict[str, pl.DataFrame]) -> bool:
        df1, e1 = self.run_code(correct_code, datasets)
        df2, e2 = self.run_code(submission_code, datasets)
        correct = self._compare_dataframes(df1, df2)
        return correct, f"e1: {e1}, e2: {e2}", df2.to_pandas().head(10).to_json()
