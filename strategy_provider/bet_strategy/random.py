import logging
import random

from strategy_provider.common.base_bet_strategy import BaseBetStrategy
from strategy_provider.common.decision import Bet
from strategy_provider.common.decision import Decision
from util.singleton import Singleton
from banker.objects import GambleInfo


class Random(BaseBetStrategy, metaclass=Singleton):
    """
    Strategy Description:
        Randomly pick up and bet a valid game.
    """

    def __init__(self):
        super().__init__("Random")
        self.candidate = [
            Bet(banker_side="local", bet_type="spread_point", result="guest"),
            Bet(banker_side="local", bet_type="spread_point", result="host"),
            Bet(banker_side="local", bet_type="total_point", result="guest"),
            Bet(banker_side="local", bet_type="total_point", result="host"),
            Bet(banker_side="local", bet_type="original", result="guest"),
            Bet(banker_side="local", bet_type="original", result="host"),
        ]

    def get_decisions(self, gamble_info_list: [GambleInfo]):
        logging.debug("get decision")
        decisions = []

        while gamble_info_list:
            gamble_info = random.choice(gamble_info_list)
            decision = Decision(
                game_type=gamble_info.game_type,
                game_date=gamble_info.game_date,
                gamble_id=gamble_info.gamble_id,
                bet=random.choice(self.candidate),
            )
            decisions.append(decision)
            break

        return decisions
