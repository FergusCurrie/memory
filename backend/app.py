import logging
from .db.cards import (
    create_card,
    create_review,
    delete_card_and_reviews,
    get_all_cards,
    get_all_reviews,
    update_card_in_db,
)
from .db.sync import sync_db_to_azure
from .scheduling.basic_scheduler import get_todays_reviews
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", filename="app.log", filemode="a"
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


class CardCreate(BaseModel):
    question: str
    answer: str


class ReviewCreate(BaseModel):
    card_id: int
    result: bool


class CardUpdate(BaseModel):
    question: str
    answer: str


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


@app.put("/api/cards/{card_id}")
async def update_card(card_id: int, card: CardUpdate):
    logger.info(f"Updating card {card_id}")
    try:
        updated_card = update_card_in_db(card_id, card.question, card.answer)
        return {"message": f"Card {card_id} updated successfully", "card": updated_card}
    except Exception as e:
        logger.error(f"Error updating card {card_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.delete("/api/cards/{card_id}")
async def delete_card(card_id: int):
    logger.info(f"Deleting card {card_id}")
    try:
        delete_card_and_reviews(card_id)
        return {"message": f"Card {card_id} and its reviews deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/cards")
async def add_card(card: CardCreate):
    try:
        card_id = create_card(card.question, card.answer)
        return {"id": card_id, "message": "Card created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/cards")
async def get_cards():
    logger.info("Getting all cards")
    try:
        cards = get_all_cards()
        logger.info(f"Cards: {cards}")
        return {"cards": cards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/cards_to_review")
async def get_cards_to_review():
    logger.info("Getting cards to review")
    try:
        cards_to_review = get_todays_reviews(get_all_cards(), get_all_reviews())
        logger.info(f"Cards to review: {cards_to_review}")
        return {"cards": cards_to_review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/reviews")
async def get_reviews():
    logger.info("Getting all reviews")
    try:
        reviews = get_all_reviews()
        logger.info(f"Reviews: {reviews}")
        return {"reviews": reviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/reviews")
async def create_review_route(review: ReviewCreate):
    try:
        review_id = create_review(review.card_id, review.result)
        return {"id": review_id, "message": "Review created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# Catch-all route for React Router
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    logger.info(f"Serving React app for path: {full_path}")
    return FileResponse("static/index.html")
