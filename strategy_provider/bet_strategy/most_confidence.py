from strategy_provider.bet_strategy.confidence_base import ConfidenceBase
from strategy_provider.common.base_bet_strategy import BaseStrategy


class MostConfidence(BaseStrategy):
    """
    To bet only the most confidence gamble.
    """

    def __init__(self, put_strategy, confidence_threshold=500):
        super().__init__("Most Confidence", put_strategy)
        self.threshold = confidence_threshold
        self.reference_group = "top_100"
        self.parameters = {"threshold": self.threshold, "group": self.reference_group}
        self.confidence_base = ConfidenceBase(put_strategy, self.threshold)
        self.game_type_sensitive = False

    def get_decisions(self, gambler, gamble_info):
        decisions = self.confidence_base.get_decisions(gambler, gamble_info)
        if decisions:
            return [max(decisions, key=lambda d: d.confidence)]
        else:
            return []