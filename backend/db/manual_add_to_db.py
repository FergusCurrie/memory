import os
import pandas as pd
from .db_helpers import get_db


def create_basic_code_compleition(dataframe_head, dataframe_target, description) -> int:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO code_completion (dataframe_header, resulting_dataframe, description) VALUES (?, ?, ?)",
        (dataframe_head.to_json(), dataframe_target.to_json(), description),
    )
    conn.commit()
    card_id = cursor.lastrowid
    conn.close()
    return card_id


if __name__ == "__main__":
    print(os.listdir())
    df = pd.read_csv("backend/code_completion/data/contoso_sales.csv")
    head = df.head()
    target = head
    description = "hello blah blah"
    print(head.to_json())
    create_basic_code_compleition(head, target, description)
