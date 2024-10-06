# import logging
# import traceback
# from ..db import get_all_reviews
# from ..scheduling.sm2_algorithm import sm2_algorithm
# from .db.problems import get_problem_for_polars

# # from .scheduling.basic_scheduler import get_todays_reviews
# # from .scheduling.basic_scheduler import get_todays_reviews
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel

# # from .scheduling.basic_scheduler import get_todays_reviews
# router = APIRouter()

# logger = logging.getLogger(__name__)


# class PlaceholderReview(BaseModel):
#     problem_id: int
#     result: bool


# class ReviewCreate(BaseModel):
#     problem_id: int
#     result: bool


# @router.post("/reviews")
# async def reviews(review: ReviewCreate):
#     try:
#         review_id = add_review(review.problem_id, review.result)
#         return {"id": review_id, "message": "Review created successfully"}
#     except Exception as e:
#         logger.error(f"Error adding review: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e)) from e


# @router.delete("/{review_id}")
# async def delete_reveiw(review_id: int):
#     logger.info(f"Deleting review {review_id}")
#     try:
#         delete_review(review_id)
#         return {"message": f"Review {review_id} and its reviews deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) from e


# @router.get("/get_next_problem")
# async def get_next_problem():
#     try:
#         # data = get_problem_for_polars(1)
#         problem_ids = get_all_problem_ids()
#         problems = []
#         logger.info(problem_ids)
#         for pid in problem_ids:
#             logger.info(pid)
#             problems.append(get_problem_for_polars(pid))
#         to_review = sm2_algorithm(problems, get_all_reviews())
#         data = to_review[0]

#         return {
#             "problem_type": "polars",
#             "problem_id": data["problem_id"],
#             "code_default": data["default_code"],
#             "datasets": data["dataset_headers"],
#             "description": data["description"],
#         }
#     except Exception as e:
#         logger.error(f"Error getting next problem: {traceback.format_exc()}")
#         raise HTTPException(status_code=500, detail=str(e)) from e
