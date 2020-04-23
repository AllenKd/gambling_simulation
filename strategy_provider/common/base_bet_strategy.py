from abc import ABC
from config.logger import get_logger


class BaseStrategy(ABC):
    def __init__(self, game_type, name, put_strategy):
        self.logger = get_logger(self.__class__.__name__)
        self.game_type = game_type
        self.name = name
        self.put_strategy = put_strategy
        self.parameters = None

    def get_decisions(self, gambler, gamble_info):
        pass
