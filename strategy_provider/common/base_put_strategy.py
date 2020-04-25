from abc import abstractmethod

from config.logger import get_logger
from util.singleton import SingletonABCMeta


class BasePutStrategy(metaclass=SingletonABCMeta):
    def __init__(self, name):
        self.logger = get_logger(self.__class__.__name__)
        self.name = name
        self.parameters = None

    @abstractmethod
    def get_unit(self, gambler, base_strategy, **kwargs):
        return NotImplementedError
