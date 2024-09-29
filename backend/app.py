import logging
from .db.problems import add_review, delete_review, get_problem_for_polars
from .db.sync import sync_db_to_azure
from .routes import card_routes, code_routes

# from .scheduling.basic_scheduler import get_todays_reviews
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

logging.basicConfig(
    level=logging.DEBUG,  # vs DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a",
)

# Set up logging
logger = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(card_routes.router, prefix="/api/card")
app.include_router(code_routes.router, prefix="/api/code")


@app.get("/")
def root():
    return FileResponse("static/index.html")


class PlaceholderReview(BaseModel):
    problem_id: int
    result: bool


class ReviewCreate(BaseModel):
    problem_id: int
    result: bool


@app.post("/api/reviews")
async def reviews(review: ReviewCreate):
    try:
        review_id = add_review(review.problem_id, review.result)
        return {"id": review_id, "message": "Review created successfully"}
    except Exception as e:
        logger.error(f"Error adding review: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/get_next_problem")
async def get_next_problem():
    try:
        data = get_problem_for_polars(1)

        return {
            "problem_type": "polars",
            "problem_id": data["problem_id"],
            "code_default": data["default_code"],
            "datasets": data["dataset_headers"],
            "description": data["description"],
        }
    except Exception as e:
        logger.error(f"Error getting next problem: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/sync_db")
async def sync_db(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(sync_db_to_azure)
        return {"message": "Database sync started in the background"}
    except Exception as e:
        logger.error(f"Error starting database sync: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


####################################### DELETE #######################################


@app.delete("/api/reviews/{review_id}")
async def delete_reveiw(review_id: int):
    logger.info(f"Deleting review {review_id}")
    try:
        delete_review(review_id)
        return {"message": f"Review {review_id} and its reviews deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


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
