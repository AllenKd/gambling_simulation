from config.logger import get_logger
from strategy_provider.base_strategy import BaseStrategy
from strategy_provider.decision import Bet
from strategy_provider.decision import Decision


# Target: 1st game of local point threshold, double bet if lose, otherwise 1
class FooDouble(BaseStrategy):
    def __init__(self, game_type, name):
        self.logger = get_logger(self.__class__.__name__)
        self.game_type = game_type
        self.name = name

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
                        bets=[self.get_bet(gambler)],
                    )
                )
                break
        return decisions

    def get_bet(self, gambler):
        self.logger.debug("getting bet")
        unit = 1
        for r in gambler.decision_history[::-1]:
            if r.match:
                break
            else:
                unit *= 2
        return Bet(banker_side="local", bet_type="total_point", result=True, unit=unit)
