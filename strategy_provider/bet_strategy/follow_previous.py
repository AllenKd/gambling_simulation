from strategy_provider.common.base_bet_strategy import BaseBetStrategy
from strategy_provider.common.decision import Bet
from strategy_provider.common.decision import Decision, get_confidence
from strategy_provider.bet_strategy.random import Random
import logging
from util.singleton import Singleton


class FollowPrevious(BaseBetStrategy, metaclass=Singleton):
    """
    Strategy Description:
        Follow the previous gamble result.
    """

    def __init__(self):
        super().__init__("Follow Previous")
        self.reference_group = "all_member"

    def get_decisions(self, gambler, gamble_info):
        logging.debug("get decision")
        if gambler.decision_history:
            last_bet = gambler.decision_history[-1].bet
        else:
            logging.debug("gambler has no decision history, make random decision")
            return Random().get_decisions()

        decisions = []
        for info in gamble_info:
            if info.game_type == self.game_type and info.is_valid(
                self.banker_side, self.bet_type
            ):
                try:
                    p = [
                        p for p in info.prediction if p["group"] == self.reference_group
                    ][0]
                    confidence = get_confidence(p[self.banker_side][self.bet_type])
                except KeyError:
                    logging.warning(
                        f"cannot get response info, skip it, info: {info}, banker side: {self.banker_side}, gamble type: {self.bet_type}"
                    )
                    continue
                except AssertionError:
                    logging.warning(
                        f"unable to get confidence index, banker side: {self.banker_side}, gamble type: {self.bet_type}, info: {info}"
                    )
                    continue
                decision = Decision(
                    game_type=self.game_type,
                    game_date=info.game_date,
                    gamble_id=info.gamble_id,
                    bet=last_bet,
                    confidence=confidence.index,
                )
                decisions.append(decision)
                break
        return decisions
