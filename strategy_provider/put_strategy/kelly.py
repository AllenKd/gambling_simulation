from strategy_provider.common.base_put_strategy import BasePutStrategy
from util.util import Util


class Kelly(BasePutStrategy):
    """
    Strategy Description:
        Bet according to Kelly Formula

    Suitable Bet Strategies:
        One bet(decision) per day and with confidence.
    """

    def __init__(self):
        super().__init__("Kelly")

    def get_unit(self, gamble_info, decision, gambler, base_strategy, **kwargs):
        response = gamble_info.handicap[decision.bet.banker_side][decision.bet.type][
            "response"
        ][decision.bet.result]
        if hasattr(decision, 'confidence'):
            win_prob = Util.confidence_to_prob(decision.confidence)
            bet_ratio = (win_prob * (response + 1) - 1) / response

            # do not bet if the ratio less than 0
            bet_ratio = max(bet_ratio, 0)
            self.logger.debug(f"bet ratio: {bet_ratio}")
            return int(gambler.principle * bet_ratio)
        else:
            self.logger.warn("no confidence for reference, return 1")
            return 1
