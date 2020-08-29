import logging
from abc import abstractmethod, ABC


class BaseStrategy(ABC):
    def __init__(self, name, put_strategy):
        self.name = name
        self.put_strategy = put_strategy
        self.parameters = None
        logging.debug(
            f"strategy initialized: {self.name}, put strategy: {self.put_strategy.name}"
        )

    @abstractmethod
    def get_decisions(self, gambler, gamble_info):
        return NotImplementedError
