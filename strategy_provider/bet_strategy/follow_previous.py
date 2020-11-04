from strategy_provider.common.base_bet_strategy import BaseBetStrategy
from strategy_provider.common.decision import Bet
from strategy_provider.common.decision import Decision, confidence_index
import logging


class FollowPrevious(BaseBetStrategy):
    """
    Strategy Description:
        Follow the previous gamble result.
    """

    def __init__(
        self,
        banker_side="local",
        game_type="NBA",
        bet_type="total_point",
        result="over",
    ):
        super().__init__("Follow Previous")
        self.banker_side = banker_side
        self.game_type = game_type
        self.bet_type = bet_type
        self.result = result
        self.reference_group = "all_member"

    def get_decisions(self, gambler, gamble_info):
        logging.debug("get decision")
        if gambler.decision_history:
            last_bet = gambler.decision_history[-1].bet
        else:
            logging.debug("gambler has no decision history, make default decision")
            last_bet = Bet(
                banker_side=self.banker_side,
                bet_type=self.bet_type,
                result=self.result,
                unit=1,
            )

        decisions = []
        for info in gamble_info:
            if info.game_type == self.game_type and info.is_valid(
                self.banker_side, self.bet_type
            ):
                try:
                    p = [
                        p for p in info.prediction if p["group"] == self.reference_group
                    ][0]
                    confidence = confidence_index(p[self.banker_side][self.bet_type])
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
