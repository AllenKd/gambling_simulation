from strategy_provider.bet_strategy.confidence_base import ConfidenceBase
from strategy_provider.common.base_bet_strategy import BaseStrategy


class MostConfidence(BaseStrategy):
    """
    To bet only the most confidence gamble.
    """

    def __init__(self, game_type, put_strategy, confidence_threshold=100):
        super().__init__(game_type, "Most Confidence", put_strategy)
        self.threshold = confidence_threshold
        self.reference_group = "all_member"
        self.parameters = {"threshold": self.threshold, "group": self.reference_group}
        self.confidence_base = ConfidenceBase(game_type, put_strategy, self.threshold)

    def get_decisions(self, gambler, gamble_info):
        decisions = self.confidence_base.get_decisions(gambler, gamble_info)
        if decisions:
            return [max(decisions, key=lambda d: d.confidence)]
        else:
            return []
