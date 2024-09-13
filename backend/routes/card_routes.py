import logging
import traceback
from ..db.cards import create_card, get_all_cards, get_note_id_from_card_id, update_card_in_db
from ..db.notes import create_review, delete_note, get_all_reviews
from ..scheduling.sm2_algorithm import sm2_algorithm

# from .scheduling.basic_scheduler import get_todays_reviews
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)


router = APIRouter()


class ReviewCreate(BaseModel):
    card_id: int
    result: bool


class CardUpdate(BaseModel):
    question: str
    answer: str


class CardCreate(BaseModel):
    question: str
    answer: str
    type: str


####################################### GET #######################################


@router.get("/cards")
async def get_cards():
    logger.info("Getting all cards")
    try:
        cards = get_all_cards()
        logger.info(f"Cards: {cards}")
        return {"cards": cards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/cards_to_review")
async def get_cards_to_review():
    logger.info("Getting cards to review")
    try:
        cards_to_review = sm2_algorithm(get_all_cards(), get_all_reviews())
        logger.info(f"Cards to review: {cards_to_review}")
        return {"cards": cards_to_review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/reviews")
async def get_reviews():
    logger.info("Getting all card reviews")
    try:
        reviews = get_all_reviews()
        logger.info(f"Reviews: {reviews}")
        return {"reviews": reviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


####################################### POST #######################################


@router.post("/reviews")
async def create_review_route(review: ReviewCreate):
    try:
        note_id = get_note_id_from_card_id(review.card_id)
        review_id = create_review(note_id, review.result)
        return {"id": review_id, "message": "Review created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/cards")
async def add_card(card: CardCreate):
    try:
        card_id = create_card(card)
        return {"id": card_id, "message": "Card created successfully"}
    except Exception as e:
        logger.error(f"An error occurred in sm2_algorithm:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


####################################### PUT #######################################


@router.put("/cards/{card_id}")
async def update_card(card_id: int, card: CardUpdate):
    logger.info(f"Updating card {card_id}")
    try:
        updated_card = update_card_in_db(card_id, card.question, card.answer)
        return {"message": f"Card {card_id} updated successfully", "card": updated_card}
    except Exception as e:
        logger.error(f"Error updating card {card_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


####################################### DELETE #######################################


@router.delete("/cards/{card_id}")
async def delete_card(card_id: int):
    logger.info(f"Deleting card {card_id}")
    try:
        note_id = get_note_id_from_card_id(card_id)
        delete_note(note_id)
        return {"message": f"Card {card_id} and its reviews deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
