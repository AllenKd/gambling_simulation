from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    def get_decision(self, gambler, gamble_info):
        pass
