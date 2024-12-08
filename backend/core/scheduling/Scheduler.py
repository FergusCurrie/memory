from .sm2_algorithm import sm2_check_problem, sm2_get_next_review
from datetime import date, datetime


class Scheduler:
    def __init__(self):
        pass

    def check_problem_ready_for_review(self, problem, reviews):
        """Pass a problem and it's reviews. A boolean is returned if this is ready for review.

        Args:
            card (_type_): _description_
            reviews (_type_): _description_
        """
        reviews_dicts = [r.to_dict() for r in reviews]
        return sm2_check_problem(problem, reviews_dicts)

    def get_next_review_date(self, problem, reviews):
        reviews_dicts = [r.to_dict() for r in reviews]
        x = sm2_get_next_review(problem, reviews_dicts)
        if isinstance(x, bool):
            x = datetime.now().date()
        assert isinstance(x, date), f"{type(x)}"
        return x
