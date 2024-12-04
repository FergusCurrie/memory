import logging
import traceback
from .core.code_execution.check_code import run_code_against_test, run_code_to_check_results_for_card_creation
from .crud import get_dataset, list_available_datasets
from .db.problem_model import get_problem_for_polars
from .db.sync import sync_db_to_azure
from .logging_config import LOGGING_CONFIG
from .routes import problem_routes, review_routes

# from .scheduling.basic_scheduler import get_todays_reviews
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

logging.config.dictConfig(LOGGING_CONFIG)


# Set up logging
logger = logging.getLogger(__name__)


app = FastAPI()

from sqlalchemy import create_engine

conn_url = "postgresql+psycopg2://ferg234e1341:32rsrg5ty3t%gst42@postgres_db/memory_db"

engine = create_engine(conn_url)
from sqlalchemy.orm import Session

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
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


# class TestCodeSubmissionNew(BaseModel):
#     code: str
#     dataset_name: str
#     problem_type: str


# @app.post("/test/api/code/test_code")
# async def submit_code(code_submission: TestCodeSubmissionNew):
#     try:

#         problem = get_problem_for_polars(code_submission.problem_id)
#         passed, result_head, error = run_code_against_test(problem=problem, code_submission=code_submission)
#         return {"passed": passed, "result_head": result_head, "error": error}
#     except Exception as e:
#         logger.error(f"An error occurred in code compleition:\n{traceback.format_exc()}")
#         raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/code/test_code")
async def submit_code(code_submission: TestCodeSubmission):
    try:
        problem = get_problem_for_polars(code_submission.problem_id)
        passed, result_head, error = run_code_against_test(problem=problem, code_submission=code_submission)
        return {"passed": passed, "result_head": result_head, "error": error}
    except Exception as e:
        logger.error(f"An error occurred in code compleition:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/code/check_creation_code")
async def check_code_for_creation(code_submission: CheckCodeForCreation):
    """Route for checking new card

    Args:
        code_submission (CheckCodeForCreation): _description_

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        logger.info(code_submission)
        datasets = {name: get_dataset(Session(engine), name) for name in code_submission.dataset_names}
        executed_df, error = run_code_to_check_results_for_card_creation(
            code_submission.code, datasets, code_submission.preprocessing_code, code_submission.problem_type
        )
        logger.info(executed_df.head(10).to_pandas().to_json())
        return {"result_head": executed_df.head(10).to_pandas().to_json()}
    except Exception as e:
        logger.error(f"An error occurred in code compleition:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/sync_db")
async def sync_db(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(sync_db_to_azure)
        return {"message": "Database sync started in the background"}
    except Exception as e:
        logger.error(f"Error starting database sync: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/available_datasets")
async def get_available_datasets():
    logger.info("Getting all available datasets")
    try:
        # datasets = ["x"]
        d = list_available_datasets(Session(engine))
        logger.info(d)
        return {"datasets": d}
    except Exception as e:
        logger.error(f"An error occurred adding code:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


####################################### DELETE #######################################


# # Catch-all route for React Router
# @app.get("/{full_path:path}")
# async def serve_react_app(full_path: str):
#     logger.info(f"Serving React app for path: {full_path}")
#     return FileResponse("static/index.html")


@app.middleware("http")
async def serve_react_or_api(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return FileResponse("static/index.html")
    return response
