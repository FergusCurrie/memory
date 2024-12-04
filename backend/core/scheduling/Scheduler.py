from abc import ABC, abstractmethod


class Scheduler(ABC):
    @abstractmethod
    def check_ready_for_review(self):
        pass
