import logging
import pandas as pd
import traceback
from .crud import create_dataset, get_code_for_problem, get_dataframes_for_problem, get_dataset, list_available_datasets
from .logging_config import LOGGING_CONFIG
from .routes import problem_routes, review_routes
from backend.core.code_execution.CheckPolarsCode import CheckPolarsCode
from backend.dbs.postgres_connection import get_postgres_db
from backend.dbs.postgres_upload_csv import add_dataset_pg
from backend.dbs.tsql_upload_csv import add_dataset_tsql

# from .scheduling.basic_scheduler import get_todays_reviews
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from io import StringIO
from pydantic import BaseModel
from sqlalchemy.orm import Session

logging.config.dictConfig(LOGGING_CONFIG)


# Set up logging
logger = logging.getLogger(__name__)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"],  # Add this line
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(problem_routes.router, prefix="/api/problem")
app.include_router(review_routes.router, prefix="/api/review")


@app.get("/")
def root():
    return FileResponse("static/index.html")


class CheckCodeForCreation(BaseModel):
    code: str
    preprocessing_code: str
    dataset_names: list
    problem_type: str


class TestCodeSubmission(BaseModel):
    problem_id: int
    code: str


@app.post("/api/code/test_code")
async def submit_code(code_submission: TestCodeSubmission, db: Session = Depends(get_postgres_db)):
    try:
        problem_id = code_submission.problem_id
        dataframes = get_dataframes_for_problem(db, problem_id)
        code = get_code_for_problem(db, problem_id)[0]

        checker = CheckPolarsCode()
        passed, error, result_head = checker.compare_code(code.code, code_submission.code, dataframes)
        logger.info({"passed": passed, "result_head": result_head, "error": error})
        return {"passed": passed, "result_head": result_head, "error": error}
    except Exception as e:
        logger.error(f"An error occurred in code compleition:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/code/check_creation_code")
async def check_code_for_creation(code_submission: CheckCodeForCreation, db: Session = Depends(get_postgres_db)):
    """Route for checking new card

    Args:
        code_submission (CheckCodeForCreation): _description_

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        datasets = {name: get_dataset(db, name) for name in code_submission.dataset_names}
        checker = CheckPolarsCode()
        executed_df, error = checker.run_code(code_submission.code, datasets)
        logger.info(executed_df.head(10).to_pandas().to_json())
        return {"result_head": executed_df.head(10).to_pandas().to_json()}
    except Exception as e:
        logger.error(f"An error occurred in code compleition:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/available_datasets")
async def get_available_datasets(db: Session = Depends(get_postgres_db)):
    logger.info("Getting all available datasets")
    try:
        # datasets = ["x"]
        d = list_available_datasets(db)
        logger.info(d)
        return {"datasets": d}
    except Exception as e:
        logger.error(f"An error occurred adding code:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.middleware("http")
async def serve_react_or_api(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return FileResponse("static/index.html")
    return response


def validate_file_extension(filename: str) -> bool:
    return filename.lower().endswith(".csv")


ALLOWED_EXTENSIONS = {"csv"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit


@app.post("/api/upload-csv")
async def upload_csv(
    file: UploadFile = File(...), db: Session = Depends(get_postgres_db), db_tsql: Session = Depends(get_postgres_db)
):
    try:
        # Validate file extension
        if not validate_file_extension(file.filename):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")

        dataset_name = file.filename.replace(".csv", "")
        # Read the file content
        contents = await file.read()
        # Check file size
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds maximum limit of 10MB")
        # Validate CSV structure (optional)
        try:
            df = pd.read_csv(StringIO(contents.decode("utf-8")))
            add_dataset_pg(dataset_name, df)
            add_dataset_tsql(dataset_name, df)
            create_dataset(db, dataset_name)
            logger.info(f"Finished adding new dataset {dataset_name}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")

        return {"result": True}

    except HTTPException:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")
