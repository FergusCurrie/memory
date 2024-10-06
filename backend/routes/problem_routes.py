import logging
import traceback
from ..db.problem_model import add_new_polars_problem, get_all_problem_ids, get_problem_for_polars
from ..db.review_model import add_review, get_all_reviews, get_review
from ..scheduling.sm2_algorithm import sm2_algorithm
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ProblemCreate(BaseModel):
    description: str
    code: str
    dataset_names: list
    preprocessing_code: str
    default_code: str


router = APIRouter()


@router.post("/")
def create_problem(problem: ProblemCreate):
    try:
        add_new_polars_problem(
            code=problem.code,
            problem_description=problem.description,
            datasets=problem.dataset_names,
            preprocessing_code=problem.preprocessing_code,
            code_start=problem.default_code,
        )
        return {"result": True}
    except Exception as e:
        logger.error(f"An error occurred in code compleition:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/")
def read_problems(skip: int = 0, limit: int = 100):
    problem_ids = get_all_problem_ids()
    problems = [get_problem_for_polars(pid[0]) for pid in problem_ids[skip : skip + limit]]
    return problems


@router.get("/get_next_problem")
def get_next_problem():
    problem_ids = get_all_problem_ids()
    logger.info(f"My problem is are :{problem_ids}")
    problems = [get_problem_for_polars(pid[0]) for pid in problem_ids]
    logger.info(f"My problem is are :{problems}")
    reviews = get_all_reviews()
    next_ = sm2_algorithm(problems, reviews)
    if len(next_) == 0:
        return {"problems": []}
    next_ = next_[0]
    logger.info(next_)
    return {
        "problems": [
            {
                "problem_type": "polars",
                "problem_id": next_["problem_id"],
                "code_default": next_["default_code"],
                "datasets": next_["dataset_headers"],
                "description": next_["description"],
            }
        ]
    }


@router.get("/{problem_id}")
def read_problem(problem_id: int):
    problem = get_problem_for_polars(problem_id)
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@router.post("/{problem_id}/reviews")
def create_review_for_problem(problem_id: int, review):
    review_id = add_review(problem_id=problem_id, result=review.result)
    if review_id is None:
        raise HTTPException(status_code=500, detail="Failed to create review")
    return get_review(review_id)
