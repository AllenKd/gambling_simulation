import logging

from banker.objects import GambleInfo
from strategy_provider.bet_strategy.confidence_base import ConfidenceBase
from strategy_provider.common.base_bet_strategy import BaseBetStrategy
from strategy_provider.common.decision import Decision
from util.singleton import Singleton


class MostConfidence(BaseBetStrategy, metaclass=Singleton):
    """
    To bet only the most confidence game.
    """

    def __init__(self, confidence_threshold=1):
        super().__init__("Most Confidence")
        self.threshold = confidence_threshold

        logging.debug("most confidence initialized")

    def get_decisions(self, gamble_info_list: [GambleInfo]) -> [Decision]:
        decisions = ConfidenceBase(self.threshold).get_decisions(gamble_info_list)
        if decisions:
            return [max(decisions, key=lambda d: d.confidence)]
        else:
            return []
