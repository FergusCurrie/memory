import logging
import pandas as pd
from backend.dbs.postgres_connection import get_postgres_conn

logger = logging.getLogger(__name__)


def add_dataset_pg(dataset_name: str, df: pd.DataFrame):
    try:
        df.to_sql(
            name=dataset_name,
            con=get_postgres_conn(),
            if_exists="fail",  # Raise error if exists
            index=False,
            method="multi",
        )
        logger.info(f"Added PG table {dataset_name}")
    except Exception as e:
        logger.info(f"PG table already exists {dataset_name}... {e}")
