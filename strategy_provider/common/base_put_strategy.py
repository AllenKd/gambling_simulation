from abc import ABC
from config.logger import get_logger


class BasePutStrategy(ABC):
    def __init__(self, name):
        self.logger = get_logger(self.__class__.__name__)
        self.name = name
        self.parameters = None

    def get_unit(self, gambler, base_strategy, **kwargs):
        self.logger.debug(f"get put unit")
        pass
