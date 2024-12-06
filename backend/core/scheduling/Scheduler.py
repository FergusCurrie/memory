from .sm2_algorithm import sm2_check_problem


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
