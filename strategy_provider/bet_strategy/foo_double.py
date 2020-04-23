from strategy_provider.base_strategy import BaseStrategy
from strategy_provider.decision import Bet
from strategy_provider.decision import Decision


# Target: 1st game of local point threshold, double bet if lose, otherwise 1
class FooDouble(BaseStrategy):
    def __init__(self, game_type, put_strategy):
        super().__init__(game_type, "Foo Double", put_strategy)

    def get_decision(self, gambler, gamble_info):
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
