import logging
import pandas as pd
from backend.dbs.tsql_connection import get_tsql_conn

logger = logging.getLogger(__name__)


def add_dataset_tsql(dataset_name: str, df: pd.DataFrame):
    try:
        df.to_sql(
            name=dataset_name,
            con=get_tsql_conn(),
            if_exists="fail",  # Raise error if exists
            index=False,
            method="multi",
        )
        logger.info(f"Added TSQL table {dataset_name}")
    except Exception as e:
        logger.info(f"TSQL table already exists {dataset_name}... {e}")
