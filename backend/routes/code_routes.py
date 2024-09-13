import logging
import traceback
from ..code_completion.check_code import run_code_against_test, run_code, get_pandas_header
from ..db.code_completion import get_a_code_completition, get_all_codes, get_note_id_from_code_id, add_code_problem_to_db
from ..db.notes import create_review, get_all_reviews
from ..scheduling.sm2_algorithm import sm2_algorithm

# from .scheduling.basic_scheduler import get_todays_reviews
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)


router = APIRouter()


class ReviewCreate(BaseModel):
    code_id: int
    result: bool


class CodeSubmission(BaseModel):
    code: str
    code_id: int


class TestCode(BaseModel):
    code: str
    dataset_name: str

class CreateCode(BaseModel):
    description: str
    dataset_name: str
    code: str

class GetHeader(BaseModel):
    dataset_name: str

####################################### GET #######################################


@router.get("/code_to_review")
async def get_code_to_review():
    logger.info("Getting codes to review")
    try:
        codes_to_review = sm2_algorithm(get_all_codes(), get_all_reviews())
        logger.info(codes_to_review)
        return {"codes": codes_to_review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/get_data_header")
async def get_data_header(dataset_name: str):
    logger.info(f"Running get_data_header for dataset: {dataset_name}")
    try:
        return {"header": get_pandas_header(dataset_name)}
    except Exception as e:
        logger.error(f"Error in get_data_header: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e

####################################### POST #######################################

@router.post("/add_code")
async def add_code(cc: CreateCode):
    try:
        description = cc.description
        dataset_name = cc.dataset_name
        code = cc.code
        note_id = add_code_problem_to_db(description, dataset_name, code)
        return {"id": note_id, "message": "Code created successfully"}
    except Exception as e:
        logger.error(f"An error occurred adding code:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/reviews")
async def create_review_route(review: ReviewCreate):
    try:
        code_id = review.code_id
        note_id = get_note_id_from_code_id(code_id)
        review_id = create_review(note_id, review.result)
        return {"id": review_id, "message": "Review created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/submit_code")
async def submit_code(code_submission: CodeSubmission):
    try:
        code_compleition_row = get_a_code_completition(code_submission.code_id)
        passed, result_head = run_code_against_test(
            code_completion_row=code_compleition_row, code_submission=code_submission
        )
        return {"passed": passed, "result_head": result_head}
    except Exception as e:
        logger.error(f"An error occurred in code compleition:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/test_code")
async def test_code(code: TestCode):
    try:
        logger.info('TESTTING code ')
        executed_df = run_code(code.code, f'backend/code_completion/data/{code.dataset_name}')
        return {"result_head": executed_df.head(10).to_json()}
    except Exception as e:
        logger.error(f"An error occurred in code compleition:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) from e
