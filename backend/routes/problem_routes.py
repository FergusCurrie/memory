import logging
import traceback
from ..db.problem_model import add_new_polars_problem, delete_problem, get_all_problem_ids, get_problem_for_polars, update_problem_in_db, toggle_suspend_problem
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
    problem_type: str


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
            type=problem.problem_type,
        )
        return {"result": True}
    except Exception as e:
        logger.error(f"An error occurred in code compleition:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/")
def read_problems(skip: int = 0, limit: int = 1000):
    problem_ids = get_all_problem_ids()
    problems = []
    for pid in problem_ids[skip : skip + limit]:
        data = get_problem_for_polars(pid[0]) 
        data['is_suspended'] = True if pid[1] == 'suspended' else False
        problems.append(data)
    return problems


@router.get("/get_next_problem")
def get_next_problem():
    problem_ids = get_all_problem_ids()
    logger.info(problem_ids)
    problem_ids = [x for x in problem_ids if x[1] == 'active']
    problems = [get_problem_for_polars(pid[0]) for pid in problem_ids]

    reviews = get_all_reviews()
    next_ = sm2_algorithm(problems, reviews)
    if len(next_) == 0:
        return {"problems": []}
    next_ = next_[0]
    #logger.info(next_["dataset_headers"])
    return {
        "problems": [
            {
                "problem_type": next_["type"],
                "problem_id": next_["problem_id"],
                "code_default": next_["default_code"],
                "datasets": next_["datasets"],
                "description": next_["description"],
                "answer": next_["code"],
            }
        ]
    }


@router.get("/get_number_problems_remaining")
def get_problems_remaining():
    problem_ids = get_all_problem_ids()
    problem_ids = [x for x in problem_ids if x[1] == 'active']
    problems = [get_problem_for_polars(pid[0]) for pid in problem_ids]
    reviews = get_all_reviews()
    next_ = sm2_algorithm(problems, reviews)
    return {"remaining": len(next_)}


@router.get("/{problem_id}")
def read_problem(problem_id: int):
    problem = get_problem_for_polars(problem_id)
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@router.put("/{problem_id}")
def update_problem(problem_id: int, problem: dict):
    try:
        # Only allow updating description and code
        logger.info(f'In the updates {problem_id}')
        update_data = {
            'description': problem.get('description'),
            'code': problem.get('code')
        }
        updated_problem = update_problem_in_db(problem_id, update_data)
        logger.info(problem)
        logger.info(updated_problem['description'])
        if updated_problem is None:
            raise HTTPException(status_code=404, detail="Problem not found")
        return updated_problem
    except Exception as e:
        logger.error(f"An error occurred while updating the problem:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e
    
    
#api.post(`/api/problem/suspend/${problem.problem_id}`);
@router.post("/suspend/{problem_id}")
def do_suspend(problem_id: int):
    logger.info(f'{problem_id} FEFEFF suspending')
    try:
        toggle_suspend_problem(problem_id)
        # Add some actual logic here
        # logger.info(f"Suspending problem with ID: {problem_id}")
        # For example, you might want to update the problem's status in the database
        # update_problem_status(problem_id, 'suspended')
        return {"message": f"Problem {problem_id} suspended successfully"}
    except Exception as e:
        logger.error(f"An error occurred while suspending the problem:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


# @router.post("/{problem_id}/reviews")
# def create_review_for_problem(problem_id: int, review):
#     review_id = add_review(problem_id=problem_id, result=review.result)
#     if review_id is None:
#         raise HTTPException(status_code=500, detail="Failed to create review")
#     return get_review(review_id)


@router.delete("/{problem_id}")
def route_delete_problem(problem_id: int):
    delete_problem(problem_id)
    return {}
