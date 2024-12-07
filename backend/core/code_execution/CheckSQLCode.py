"""
Code to check a tsql query.
"""

import logging
import polars as pl
from backend.dbs.tsql_connection import get_tsql_conn
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)


class CheckSQLCode:
    def __init__(self):
        pass

    def _compare_dataframes(self, df1, df2):
        if set(df1.columns) != set(df2.columns):
            return False
        df1_sorted = df1.sort(by=df1.columns)
        df2_sorted = df2.sort(by=df2.columns)
        return df1_sorted.equals(df2_sorted)

    def _add_schema(self, code):
        if "from " in code.lower() and "dbo." not in code.lower():
            code = code.replace("from ", "from dbo.", 1)
            code = code.replace("FROM ", "FROM dbo.", 1)
        return code

    def run_code(self, code) -> [pl.DataFrame, str]:
        try:
            conn_str = get_tsql_conn()
            engine = create_engine(conn_str)
            with engine.connect() as conn:
                result = conn.execute(text(self._add_schema(code)))
                rows = result.fetchall()
                columns = result.keys()
                data = [{col: val for col, val in zip(columns, row)} for row in rows]
                df = pl.DataFrame(data)
            return df, None

        except Exception as e:
            logger.info(e)
            return None, str(e)

    def compare_code(self, correct_code: str, submission_code: str) -> bool:
        df1, e1 = self.run_code(correct_code)
        df2, e2 = self.run_code(submission_code)
        correct = self._compare_dataframes(df1, df2)
        return correct, f"e1: {e1}, e2: {e2}", df2.to_pandas().head(10).to_json()
