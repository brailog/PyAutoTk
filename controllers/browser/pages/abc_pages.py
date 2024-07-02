from abc import ABC, abstractmethod


class PageObj(ABC):
    @abstractmethod
    def open(self):
        pass
