from strategy_provider.common.base_bet_strategy import BaseStrategy
from strategy_provider.common.decision import Bet, Decision, confidence_index


class ConfidenceBase(BaseStrategy):
    def __init__(self, put_strategy, confidence_threshold=500):
        super().__init__("Confidence Base", put_strategy)
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
                            self.logger.warn(
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
                                    unit=None,
                                ),
                                confidence=confidence.index,
                            )
                            decision.bet.unit = self.put_strategy.get_unit(
                                info, decision, gambler, self
                            )

                            if decision.bet.unit:
                                self.logger.debug(f"append decision: {decision}")
                                decisions.append(decision)

        return decisions
