import logging
from .db.sync import sync_db_to_azure
from .routes import card_routes, code_routes

# from .scheduling.basic_scheduler import get_todays_reviews
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", filename="app.log", filemode="a"
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


@app.post("/api/sync_db")
async def sync_db(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(sync_db_to_azure)
        return {"message": "Database sync started in the background"}
    except Exception as e:
        logger.error(f"Error starting database sync: {str(e)}")
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
