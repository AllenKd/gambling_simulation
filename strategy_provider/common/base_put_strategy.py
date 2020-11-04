import logging
from abc import abstractmethod, ABC


class BasePutStrategy(ABC):
    def __init__(self, name: str):
        self.name = name
        logging.debug(f"put strategy initialized: {self.name}")

    @abstractmethod
    def get_unit(self, *args, **kwargs):
        return NotImplementedError
