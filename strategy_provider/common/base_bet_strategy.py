import logging
from abc import abstractmethod, ABC


class BaseBetStrategy(ABC):
    def __init__(self, name: str):
        self.name = name
        logging.debug(f"bet strategy initialized: {self.name}")

    @abstractmethod
    def get_decisions(self, *args, **kwargs):
        return NotImplementedError
