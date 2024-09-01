from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from pydantic import BaseModel
from db.cards import create_card, get_all_cards, create_review, get_all_reviews
import logging 

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a'
)

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

@app.get("/")
def root():
    return FileResponse("static/frontend/index.html")

@app.post("/api/cards")
async def add_card(card: CardCreate):
    try:
        card_id = create_card(card.question, card.answer)
        return {"id": card_id, "message": "Card created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cards")
async def get_cards():
    logger.info("Getting all cards")
    try:
        cards = get_all_cards()
        logger.info(f"Cards: {cards}")
        return {"cards": cards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews")
async def get_reviews():
    logger.info("Getting all reviews")
    try:
        reviews = get_all_reviews()
        logger.info(f"Reviews: {reviews}")
        return {"reviews": reviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reviews")
async def create_review_route(review: ReviewCreate):
    try:
        review_id = create_review(review.card_id, review.result)
        return {"id": review_id, "message": "Review created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Catch-all route for React Router
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    return FileResponse("static/frontend/index.html")

    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
