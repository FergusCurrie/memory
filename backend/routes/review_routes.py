from ..crud import create_review, get_all_reviews
from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session


class ReviewCreate(BaseModel):
    problem_id: int
    result: bool


router = APIRouter()


@router.post("/")
def add_a_review(review: ReviewCreate, db: Session = Depends(get_db)):
    review = create_review(db, problem_id=review.problem_id, result=review.result)
    if review is None:
        raise HTTPException(status_code=500, detail="Failed to create review")
    return review.to_dict()


@router.get("/")
def get_reviews(db: Session = Depends(get_db)):
    return [x.to_dict() for x in get_all_reviews(db)]


# @router.get("/{review_id}")
# def get_a_review(review_id: int):
#     db_review = get_review(review_id)
#     if db_review is None:
#         raise HTTPException(status_code=404, detail="Review not found")
#     return db_review


# @router.delete("/{review_id}")
# def route_delete_review(review_id: int):
#     db_review = get_review(review_id)
#     if db_review is None:
#         raise HTTPException(status_code=404, detail="Review not found")
#     delete_review(review_id)
#     return db_review
