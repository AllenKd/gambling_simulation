from strategy_provider.common.base_bet_strategy import BaseBetStrategy
from strategy_provider.common.decision import Bet, Decision, get_confidence


class LowResponse(BaseBetStrategy):
    """
    Bet lower response side.
    """

    def __init__(self, put_strategy):
        super().__init__("Low Response", put_strategy)
        self.game_type_sensitive = False
        self.reference_group = "all_member"

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

                    p = [
                        p for p in info.prediction if p["group"] == self.reference_group
                    ][0]
                    confidence = get_confidence(p[banker_side][gamble_type])
                except KeyError:
                    self.logger.warn(
                        f"cannot get response info, skip it, info: {info}, banker side: {banker_side}, gamble type: {gamble_type}"
                    )
                    continue
                except AssertionError:
                    self.logger.warn(
                        f"unable to get confidence index, banker side: {banker_side}, gamble type: {gamble_type}, info: {info}"
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
                    confidence=confidence.index,
                )
                decision.bet.unit = self.put_strategy.get_unit(
                    info, decision, gambler, self
                )

                if decision.bet.unit:
                    self.logger.debug(f"append decision: {decision}")
                    decisions.append(decision)
        return decisions
