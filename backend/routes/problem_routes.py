import json
import logging
import traceback
from ..core.scheduling.Scheduler import Scheduler
from ..crud import (
    add_code_to_problem,
    bury_problem,
    check_problem_buried,
    check_problem_suspended,
    create_problem,
    # get_all_non_suspended_problems,
    get_all_problems,
    get_code_for_problem,
    get_dataframes_for_problem,
    get_list_of_datasets_for_problem,
    get_problem,
    get_reviews_for_problem,
    toggle_suspend,
    update_code,
    update_problem,
)
from backend.dbs.postgres_connection import get_postgres_db
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class ProblemCreate(BaseModel):
    description: str
    code: str
    dataset_names: list
    preprocessing_code: str
    default_code: str
    problem_type: str


class Card(BaseModel):
    front: str
    back: str


router = APIRouter()


@router.post("/")
def create_a_new_problem(problem: ProblemCreate, db: Session = Depends(get_postgres_db)):
    try:
        new_prob = create_problem(db, problem.description)
        add_code_to_problem(
            db, problem.code, ",".join(problem.dataset_names), new_prob.id, problem.problem_type, problem.default_code
        )
        return {"result": True}
    except Exception as e:
        logger.error(f"An error occurred in code compleition:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/")
def get_problems(db: Session = Depends(get_postgres_db)):
    problems = get_all_problems(db)
    result = []
    for p in problems:
        problem_id = p.id
        table_name = get_list_of_datasets_for_problem(db, problem_id)[0]
        dataframes = get_dataframes_for_problem(db, problem_id)
        code = get_code_for_problem(db, problem_id)[0]
        result.append(
            {
                "problem_id": problem_id,
                "dataset_name": table_name,
                "dataset_headers": "",
                "code": code.code,
                "default_code": code.default_code,
                "preprocessing_code": "",
                "description": p.description,
                "is_suspended": check_problem_suspended(db, problem_id),
            }
        )
    return result


# @router.post("/")
# def create_problem(problem: ProblemCreate):
#     try:
#         add_new_polars_problem(
#             code=problem.code,
#             problem_description=problem.description,
#             datasets=problem.dataset_names,
#             preprocessing_code=problem.preprocessing_code,
#             code_start=problem.default_code,
#             type=problem.problem_type,
#         )
#         return {"result": True}
#     except Exception as e:
#         logger.error(f"An error occurred in code compleition:\n{traceback.format_exc()}")
#         raise HTTPException(status_code=500, detail=str(e)) from e


# @router.post("/card/create")
# def create_problem(card: Card):
#     try:
#         add_card(front=card.front, back=card.back)
#         return {"result": True}
#     except Exception as e:
#         logger.error(f"An error occurred in code compleition:\n{traceback.format_exc()}")
#         raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/get_next_problem")
def get_next_problem(db: Session = Depends(get_postgres_db)):
    try:
        problems = get_all_problems(db)
        problems = [p for p in problems if not check_problem_suspended(db, p.id) and not check_problem_buried(db, p.id)]
        # problems = get_all_non_suspended_problems(db)
        logger.info(problems)
        scheduler = Scheduler()

        problems_to_review = []
        for problem in problems:
            reviews = get_reviews_for_problem(db, problem.id)
            if scheduler.check_problem_ready_for_review(problem, reviews):
                problems_to_review.append(problem)
        logger.info(problems_to_review)
        # problem_ids = [{"problem_id": x[0], "type": x[2]} for x in problem_ids if x[1] == "active"]
        # problems = [get_problem_for_polars(pid[0]) for pid in problem_ids]

        if len(problems_to_review) == 0:
            return {"problems": []}
        next_ = problems_to_review[0]

        return {"problems": [{"problem_type": "polars", "problem_id": next_.id}]}
    except Exception as e:
        logger.error(f"An error occurred while updating the problem:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/get_number_problems_remaining")
def get_problems_remaining(db: Session = Depends(get_postgres_db)):
    try:
        problems = get_all_problems(db)
        problems = [p for p in problems if not check_problem_suspended(db, p.id) and not check_problem_buried(db, p.id)]
        scheduler = Scheduler()
        problems_to_review = []
        for problem in problems:
            reviews = get_reviews_for_problem(db, problem.id)
            if scheduler.check_problem_ready_for_review(problem, reviews):
                problems_to_review.append(problem)
        logger.info(f"problems to review: {problems_to_review}")
        return {"remaining": len(problems_to_review)}
    except Exception as e:
        logger.error(f"An error occurred while updating the problem:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/{problem_id}")
def do_update_problem(problem_id: int, problem_update: dict, db: Session = Depends(get_postgres_db)):
    try:
        logger.info(f"UPdating probl. prob id = {problem_id}, problem_update: {problem_update}")
        description = problem_update["description"]
        code = problem_update["code"]
        default_code = problem_update["default_code"]
        update_problem(db, problem_id, description)
        update_code(db, code, None, problem_id, default_code)
        # Only allow updating description and code

        return {"dnoe": True}
    except Exception as e:
        logger.error(f"An error occurred while updating the problem:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/suspend/{problem_id}")
def do_suspend(problem_id: int, db: Session = Depends(get_postgres_db)):
    logger.info(f"{problem_id} FEFEFF suspending")
    try:
        toggle_suspend(db, problem_id)
        return {"message": f"Problem {problem_id} suspended successfully"}
    except Exception as e:
        logger.error(f"An error occurred while suspending the problem:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/bury/{problem_id}")
def do_bury(problem_id: int, db: Session = Depends(get_postgres_db)):
    try:
        bury_problem(db, problem_id)
        return {"message": f"Problem {problem_id} buried successfully"}
    except Exception as e:
        logger.error(f"An error occurred while burying the problem:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


# @router.post("/{problem_id}/reviews")
# def create_review_for_problem(problem_id: int, review):
#     review_id = add_review(problem_id=problem_id, result=review.result)
#     if review_id is None:
#         raise HTTPException(status_code=500, detail="Failed to create review")
#     return get_review(review_id)


# @router.delete("/{problem_id}")
# def route_delete_problem(problem_id: int):
#     delete_problem(problem_id)
#     return {}


####### CUSTOM problem teyps


@router.get("/data_wrangling/{problem_id}")
def get_data_wrangling_problem(problem_id, db: Session = Depends(get_postgres_db)):
    try:
        # get_problem_for_polars(problem_id)
        problem = get_problem(db, problem_id)
        table_name = get_list_of_datasets_for_problem(db, problem_id)[0]
        dataframes = get_dataframes_for_problem(db, problem_id)
        code = get_code_for_problem(db, problem_id)[0]  # 1 code per prob for now

        return {
            "problems": [
                {
                    "problem_type": "polars",
                    "problem_id": problem_id,
                    "code_default": "result = (\n\tdf\n)",
                    "datasets": {
                        table_name: json.loads(dataframes[table_name].to_pandas().to_json())
                    },  # literally datasets
                    "description": problem.description,
                    "answer": code.code,
                }
            ]
        }
    except Exception as e:
        logger.error(f"An error occurred while updating the problem:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


# @router.get("/multi_choice/{problem_id}")
# def get_multi_choice_problem(problem_id):
#     try:
#         return multi_choice_generation(get_multi_choice_by_problem_id(problem_id))
#     except Exception as e:
#         logger.error(f"An error occurred while updating the problem:\n{traceback.format_exc()}")
#         raise HTTPException(status_code=500, detail=str(e)) from e


# @router.get("/card/{problem_id}")
# def get_card_problem(problem_id):
#     try:
#         return get_card_by_problem_id(problem_id)
#     except Exception as e:
#         logger.error(f"An error occurred while updating the problem:\n{traceback.format_exc()}")
#         raise HTTPException(status_code=500, detail=str(e)) from e
