from strategy_provider.common.base_bet_strategy import BaseStrategy
from strategy_provider.common.decision import Bet
from strategy_provider.common.decision import Decision


class FooDouble(BaseStrategy):
    """
    Strategy Description:
        Bet 1st game with gamble type "total point" on local banker.
    """

    def __init__(self, game_type, put_strategy):
        super().__init__(game_type, "Foo Double", put_strategy)

    def get_decisions(self, gambler, gamble_info):
        self.logger.debug("get decision")
        decisions = []
        for info in gamble_info:
            if info.game_type == self.game_type:
                decisions.append(
                    Decision(
                        game_type=self.game_type,
                        game_date=info.game_date,
                        gamble_id=info.gamble_id,
                        bet=Bet(
                            banker_side="local",
                            bet_type="total_point",
                            result="over",
                            unit=self.put_strategy.get_unit(gambler, self),
                        ),
                    )
                )
                break
        return decisions
