from ..crud import (
    create_due_date,
    create_review,
    create_review_duration,
    get_all_reviews,
    get_problem,
    get_reviews_for_problem,
)
from backend.core.scheduling.Scheduler import Scheduler
from backend.dbs.postgres_connection import get_postgres_db
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session


class ReviewCreate(BaseModel):
    problem_id: int
    result: bool
    duration_ms: float


router = APIRouter()


@router.post("/")
def add_a_review(review: ReviewCreate, db: Session = Depends(get_postgres_db)):
    new_review = create_review(db, problem_id=review.problem_id, result=review.result)
    scheduler = Scheduler()
    problem = get_problem(db, new_review.problem_id)
    reviews = get_reviews_for_problem(db, problem.id)
    due = scheduler.get_next_review_date(problem, reviews)
    create_due_date(db, problem.id, due, "sm2")
    create_review_duration(db, new_review.id, duration=review.duration_ms)
    if review is None:
        raise HTTPException(status_code=500, detail="Failed to create review")
    return new_review.to_dict()


@router.get("/")
def get_reviews(db: Session = Depends(get_postgres_db)):
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
