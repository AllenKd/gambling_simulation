from strategy_provider.common.base_bet_strategy import BaseBetStrategy
from strategy_provider.common.decision import Bet, Decision, confidence_index
import logging


class ConfidenceBaseBet(BaseBetStrategy):
    def __init__(self, confidence_threshold=500):
        super().__init__("Confidence Base")
        self.threshold = confidence_threshold
        # focus on local currently
        self.banker_side = ["local"]
        self.reference_group = "all_member"
        self.parameters = {"threshold": self.threshold, "group": self.reference_group}
        self.game_type_sensitive = False

    def get_decisions(self, gambler, gamble_info):
        decisions = []
        for info in gamble_info:
            for prediction in info.prediction:
                if prediction["group"] != self.reference_group:
                    continue
                for banker_side in self.banker_side:
                    for gamble_type, side_vote in prediction[banker_side].items():
                        try:
                            confidence = confidence_index(side_vote)
                        except AssertionError:
                            logging.warning(
                                f"unable to get confidence index, banker side: {banker_side}, gamble type: {gamble_type}, info: {info}"
                            )
                            continue
                        if confidence.index > self.threshold:
                            decision = Decision(
                                game_type=info.game_type,
                                game_date=info.game_date,
                                gamble_id=info.gamble_id,
                                bet=Bet(
                                    banker_side=banker_side,
                                    bet_type=gamble_type,
                                    result=confidence.side,
                                ),
                                confidence=confidence.index,
                            )
                            decisions.append(decision)

        return decisions
