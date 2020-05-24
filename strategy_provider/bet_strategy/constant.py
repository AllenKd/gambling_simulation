from strategy_provider.common.base_bet_strategy import BaseStrategy
from strategy_provider.common.decision import Bet
from strategy_provider.common.decision import Decision


class Constant(BaseStrategy):
    """
    Strategy Description:
        Bet 1st valid game with specified banker and game type.
    """

    def __init__(
        self,
        put_strategy,
        banker_side="local",
        game_type="NBA",
        bet_type="total_point",
        result="over",
    ):
        super().__init__("Constant", put_strategy)
        self.banker_side = banker_side
        self.game_type = game_type
        self.bet_type = bet_type
        self.result = result

    def get_decisions(self, gambler, gamble_info):
        self.logger.debug("get decision")
        decisions = []
        for info in gamble_info:
            if info.game_type == self.game_type and info.is_valid(
                self.banker_side, self.bet_type
            ):
                decision = Decision(
                    game_type=info.game_type,
                    game_date=info.game_date,
                    gamble_id=info.gamble_id,
                    bet=Bet(
                        banker_side=self.banker_side,
                        bet_type=self.bet_type,
                        result=self.result,
                        unit=None,
                    ),
                )
                decision.bet.unit = self.put_strategy.get_unit(
                    info, decision, gambler, self
                )
                if decision.bet.unit:
                    decisions.append(decision)
                break
        return decisions
