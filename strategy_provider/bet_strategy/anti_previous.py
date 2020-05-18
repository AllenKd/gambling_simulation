from strategy_provider.bet_strategy.follow_previous import FollowPrevious
from strategy_provider.common.base_bet_strategy import BaseStrategy


class AntiPrevious(BaseStrategy):
    """
    Strategy Description:
        Bet with anti side if the previous gamble.
    """

    def __init__(
        self,
        put_strategy,
        banker_side="local",
        game_type="NBA",
        bet_type="total_point",
        result="over",
    ):
        super().__init__("Anti Previous", put_strategy)
        self.banker_side = banker_side
        self.game_type = game_type
        self.bet_type = bet_type
        self.result = result

        self.anti_map = {
            "over": "under",
            "under": "over",
            "host": "guest",
            "guest": "host",
        }
        self.follow_previous = FollowPrevious(put_strategy=put_strategy)

    def get_decisions(self, gambler, gamble_info):
        self.logger.debug("get decision")
        decisions = self.follow_previous.get_decisions(gambler, gamble_info)
        if len(decisions) == 1:
            decisions[0].bet.result = self.anti_map[decisions[0].bet.result]
        return decisions
