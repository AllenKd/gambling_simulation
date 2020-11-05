import logging
import random

from banker.objects import GambleInfo
from strategy_provider.common.base_bet_strategy import BaseBetStrategy
from strategy_provider.common.decision import Bet, Decision
from util.singleton import Singleton


class LowestResponse(BaseBetStrategy, metaclass=Singleton):
    """
    Bet the lowest response side.
    """

    def __init__(self):
        super().__init__("Lowest Response")

        logging.debug("lowest response initialized")

    def get_decisions(self, gamble_info_list: [GambleInfo]):
        lowest_response = 2
        lowest_response_decisions = []
        for gamble_info in gamble_info_list:
            for game_type, info in gamble_info.gamble_info.items():
                temp_min = min(info["response"].valies())
                if temp_min < lowest_response:
                    logging.debug(f"update lowest response: {temp_min}")
                    lowest_response = temp_min
                    side = min(info["response"], key=info["response"].get)
                    lowest_response_decisions = [
                        Decision(
                            game_type=info.game_type,
                            game_date=info.game_date,
                            gamble_id=info.gamble_id,
                            bet=Bet(
                                banker_side="local", bet_type=game_type, result=side,
                            ),
                        )
                    ]
                if temp_min == lowest_response:
                    side = min(info["response"], key=info["response"].get)
                    lowest_response_decisions.append(
                        Decision(
                            game_type=info.game_type,
                            game_date=info.game_date,
                            gamble_id=info.gamble_id,
                            bet=Bet(
                                banker_side="local", bet_type=game_type, result=side,
                            ),
                        )
                    )

        decisions = [random.choice(lowest_response_decisions)]
        return decisions
