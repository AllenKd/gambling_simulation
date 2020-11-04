import logging

from strategy_provider.common.base_bet_strategy import BaseBetStrategy
from strategy_provider.common.decision import Bet
from strategy_provider.common.decision import Decision, confidence_index
import random
from util.singleton import Singleton


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

    def get_decisions(self, *args, **kwargs):
        logging.debug("get decision")
        decisions = []

        # TODO: add maximum try
        while True:
            gamble_info = random.choice(kwargs["gamble_info"])
            if not gamble_info.is_valid():
                logging.info(f"invalid game: {gamble_info}")
                continue

            decision = Decision(
                game_type=gamble_info.game_type,
                game_date=gamble_info.game_date,
                gamble_id=gamble_info.gamble_id,
                bet=random.choice(self.candidate),
            )
            decisions.append(decision)
            return decisions
