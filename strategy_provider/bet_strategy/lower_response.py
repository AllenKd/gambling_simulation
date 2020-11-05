import logging

from banker.objects import GambleInfo
from strategy_provider.common.base_bet_strategy import BaseBetStrategy
from strategy_provider.common.decision import Bet, Decision
from util.singleton import Singleton


class LowerResponse(BaseBetStrategy, metaclass=Singleton):
    """
    Bet side with lower response.
    """

    def __init__(self):
        super().__init__("Low Response")

        logging.debug("low response initialized")

    def get_decisions(self, gamble_info_list: [GambleInfo]):
        decisions = []
        for gamble_info in gamble_info_list:
            for game_type, info in gamble_info.gamble_info.items():
                resp_info = info["response"]
                side = min(resp_info, key=resp_info.get,)
                decision = Decision(
                    game_type=info.game_type,
                    game_date=info.game_date,
                    gamble_id=info.gamble_id,
                    bet=Bet(banker_side="local", bet_type=game_type, result=side),
                )
                decisions.append(decision)
        return decisions
