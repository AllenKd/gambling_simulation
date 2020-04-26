from strategy_provider.common.base_bet_strategy import BaseStrategy
from strategy_provider.common.decision import Bet
from strategy_provider.common.decision import Decision


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
                        confidence = self.confidence_index(side_vote)
                        if confidence.index > self.threshold:

                            decisions.append(
                                Decision(
                                    game_type=info.game_type,
                                    game_date=info.game_date,
                                    gamble_id=info.gamble_id,
                                    bet=Bet(
                                        banker_side=banker_side,
                                        bet_type=gamble_type,
                                        result=confidence.side,
                                        # TODO: better to deal with kwargs?
                                        unit=self.put_strategy.get_unit(
                                            gambler,
                                            self,
                                            response=info.handicap[banker_side][
                                                gamble_type
                                            ]["response"][confidence.side],
                                        ),
                                    ),
                                    confidence=confidence.index,
                                )
                            )

        return decisions

    def confidence_index(self, side_vote):
        self.logger.debug(f"start get confidence index: {side_vote}")
        side_1 = list(side_vote)[0]
        side_2 = list(side_vote)[1]

        c = Confidence

        # TODO: can be refine
        if not side_vote[side_1]["population"] and not side_vote[side_2]["population"]:
            self.logger.warn("zero vote")
        elif side_vote[side_1]["population"] > side_vote[side_2]["population"]:
            c.side = side_1
            side_vote[side_2]["population"] = side_vote[side_2]["population"] or 0.1
            c.index = (
                side_vote[side_1]["population"] / side_vote[side_2]["population"]
            ) * (side_vote[side_1]["population"] - side_vote[side_2]["population"])
        else:
            c.side = side_2
            side_vote[side_1]["population"] = side_vote[side_1]["population"] or 0.1
            c.index = (
                side_vote[side_2]["population"] / side_vote[side_1]["population"]
            ) * (side_vote[side_2]["population"] - side_vote[side_1]["population"])
        return c


class Confidence:
    gamble_type = None
    side = None
    index = 0

    def __str__(self):
        return (
            f"gamble_type: {self.gamble_type}, side: {self.side}, index: {self.index}"
        )
