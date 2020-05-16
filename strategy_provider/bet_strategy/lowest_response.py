from strategy_provider.bet_strategy.low_response import LowResponse
from strategy_provider.common.base_bet_strategy import BaseStrategy
from strategy_provider.common.decision import Bet, Decision


class LowestResponse(BaseStrategy):
    """
    Bet the lowest response side.
    """

    def __init__(self, put_strategy, confidence_threshold=500):
        super().__init__("Lowest Response", put_strategy)
        self.threshold = confidence_threshold
        self.game_type_sensitive = False
        self.low_response = LowResponse(put_strategy)

        self.side_type = [
            # ("national", "total_point"),
            # ("national", "spread_point"),
            ("local", "total_point"),
            ("local", "spread_point"),
            ("local", "original"),
        ]

    def get_decisions(self, gambler, gamble_info):
        decisions = []
        lowest_response = 2
        for info in gamble_info:
            for banker_side, gamble_type in self.side_type:
                try:
                    resp_info = info.handicap[banker_side][gamble_type]["response"]
                except KeyError:
                    self.logger.warn(
                        f"cannot get response info, skip it, info: {info}, banker side: {banker_side}, gamble type: {gamble_type}"
                    )
                    continue
                temp_min = int(min(resp_info.values()))
                if temp_min < lowest_response:
                    lowest_response = temp_min
                    side = min(resp_info, key=resp_info.get,)
                    decision = Decision(
                        game_type=info.game_type,
                        game_date=info.game_date,
                        gamble_id=info.gamble_id,
                        bet=Bet(
                            banker_side=banker_side,
                            bet_type=gamble_type,
                            result=side,
                            unit=None,
                        ),
                    )
                    decision.bet.unit = self.put_strategy.get_unit(
                        info, decision, gambler, self
                    )

                    if decision.bet.unit:
                        self.logger.debug(
                            f"update decision with lowest response: {decision}"
                        )
                        decisions = [decision]
        return decisions
