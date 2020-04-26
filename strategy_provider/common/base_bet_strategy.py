from abc import abstractmethod, ABC

from config.logger import get_logger


class BaseStrategy(ABC):
    def __init__(self, name, put_strategy):
        self.logger = get_logger(self.__class__.__name__)
        self.name = name
        self.put_strategy = put_strategy
        self.parameters = None
        self.logger.debug(f"strategy initialized: {self.name}, put strategy: {self.put_strategy.name}")

    @abstractmethod
    def get_decisions(self, gambler, gamble_info):
        return NotImplementedError
