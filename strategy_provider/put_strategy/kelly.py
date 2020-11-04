import pickle

import numpy as np

from strategy_provider.common.base_put_strategy import BasePutStrategy


class Kelly(BasePutStrategy):
    """
    Strategy Description:
        Bet according to Kelly Formula

    Suitable Bet Strategies:
        One bet(decision) per day and with confidence.
    """

    def __init__(self):
        super().__init__("Kelly")
        with open(
            "game_predictor/models/trained/confidence_to_prob/all.pkl", "rb"
        ) as model:
            self.model = pickle.load(model)

    def get_unit(self, gamble_info, decision, gambler, base_strategy, **kwargs):
        try:
            response = gamble_info.handicap[decision.bet.banker_side][
                decision.bet.type
            ]["response"][decision.bet.result]
        except KeyError:
            self.logger.error(
                f"unable to get response ratio from handicap, gamble info: {gamble_info}, decision: {decision}, do not bet"
            )
            return 0

        if hasattr(decision, "confidence"):
            win_prob = self.model.predict(
                np.array([decision.confidence]).reshape(-1, 1)
            )[0][0]
            self.logger.debug(f"win prob from model: {win_prob}")
            # avoid all in
            win_prob = min(win_prob, 0.8)
            bet_ratio = (win_prob * (response + 1) - 1) / response

            # do not bet if the ratio less than 0
            bet_ratio = max(bet_ratio, 0)
            self.logger.debug(f"bet ratio: {bet_ratio}")
            return int(gambler.capital * bet_ratio)
        else:
            self.logger.warn("no confidence for reference, return 1")
            return 1
