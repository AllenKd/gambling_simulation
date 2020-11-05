import logging

from banker.objects import GambleInfo
from strategy_provider.common.base_bet_strategy import BaseBetStrategy
from strategy_provider.common.decision import Bet, Decision
from util.singleton import Singleton


class ConfidenceBase(BaseBetStrategy, metaclass=Singleton):
    def __init__(self, confidence_threshold=1):
        super().__init__("Confidence Base")
        self.threshold = confidence_threshold

        logging.debug("confidence base initialized")

    def get_decisions(self, gamble_info_list: [GambleInfo]):
        decisions = []
        for gamble_info in gamble_info_list:
            for game_type, info in gamble_info.gamble_info.items():
                if info.confidence.index > self.threshold:
                    decision = Decision(
                        game_type=info.game_type,
                        game_date=info.game_date,
                        gamble_id=info.gamble_id,
                        bet=Bet(
                            banker_side="local",
                            bet_type=game_type,
                            result=info.confidence.result,
                        ),
                        confidence=info.confidence.index,
                    )
                    decisions.append(decision)

        return decisions
