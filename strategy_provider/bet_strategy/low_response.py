from strategy_provider.common.base_bet_strategy import BaseStrategy
from strategy_provider.common.decision import Bet, Decision


class LowResponse(BaseStrategy):
    """
    Bet lower response side.
    """

    def __init__(self, put_strategy):
        super().__init__("Low Response", put_strategy)
        self.game_type_sensitive = False

        self.side_type = [
            # ("national", "total_point"),
            # ("national", "spread_point"),
            ("local", "total_point"),
            ("local", "spread_point"),
            ("local", "original"),
        ]

    def get_decisions(self, gambler, gamble_info):
        decisions = []
        for info in gamble_info:
            for banker_side, gamble_type in self.side_type:
                try:
                    resp_info = info.handicap[banker_side][gamble_type]["response"]
                except KeyError:
                    self.logger.warn(
                        f"cannot get response info, skip it, info: {info}, banker side: {banker_side}, gamble type: {gamble_type}"
                    )
                    continue
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
                    self.logger.debug(f"append decision: {decision}")
                    decisions.append(decision)
        return decisions
