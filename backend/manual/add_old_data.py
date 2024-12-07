import pandas as pd
from backend.crud import add_code_to_problem, create_problem, create_review
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

CSV_DIR = "/workspaces/memory/memory_backups/memory_datasets/data"

conn_url = "postgresql+psycopg2://ferg234e1341:32rsrg5ty3t%gst42@postgres_db/memory_db"

engine = create_engine(conn_url)

session = Session(engine)

code = pd.read_csv("code.csv")
problem = pd.read_csv("problems.csv")
reviews = pd.read_csv("reviews.csv")
datasets = pd.read_csv("datasets.csv")

for i, row in problem.iterrows():
    if row["type"] != "polars":
        continue
    # print(row)
    datasets_i = datasets[datasets["problem_id"] == row["id"]]
    if len(datasets_i) > 1:
        continue

    dataset = datasets_i["dataset_name"].iloc[0]

    code_i = code[code["problem_id"] == row["id"]]
    review_i = reviews[reviews["problem_id"] == row["id"]]

    code_to_add = code_i["code"].iloc[0]

    desc = row["description"]

    p = create_problem(session, desc, date_created=row["date_created"])
    add_code_to_problem(session, code_to_add, dataset, p.id)
    for j, rrow in review_i.iterrows():
        create_review(session, p.id, rrow["result"], date_created=rrow["date_created"])
        pass
