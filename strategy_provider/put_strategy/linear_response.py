import logging
import math

from banker.banker import Banker
from gambler.gambler import Gambler
from strategy_provider.common.base_put_strategy import BasePutStrategy


class LinearResponse(BasePutStrategy):
    """
    Strategy Description:
        Calculate how much unit to put can resulting the response as linear since last time win the gamble.

    Suitable Bet Strategies:
        One bet(decision) per day.

    """

    def __init__(self):
        super().__init__("Linear Response")

    def get_unit(self, gambler: Gambler):
        if not gambler.decision_history:
            logging.info("empty decision history")
            return 1

        try:
            last_decision = gambler.decision_history[-1]
            response = last_decision.get_response()
        except KeyError as e:
            logging.error(f"fail to get response from decision: {e}")
            return 0
        except Exception as e:
            logging.error(f"unknown error: {e}")
            return 0

        unit = 1
        daily_expect_response = response - unit
        total_expect_response = daily_expect_response
        put_accumulation = 0

        for d in gambler.decision_history[::-1]:
            if d.match:
                break
            else:
                put_accumulation += d.bet.unit
                total_expect_response += daily_expect_response
                unit = math.ceil(
                    (total_expect_response + put_accumulation) / daily_expect_response
                )
        logging.debug(f"linear response put unit: {unit}")
        return unit
