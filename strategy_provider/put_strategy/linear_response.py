import math

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

    def get_unit(self, gamble_info, decision, gambler, bet_strategy, **kwargs):
        try:
            response = gamble_info.handicap[decision.bet.banker_side][
                decision.bet.type
            ]["response"][decision.bet.result]
        except KeyError:
            self.logger.error(
                f"unable to get response ratio from handicap, gamble info: {gamble_info}, decision: {decision}, do not bet"
            )
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
        self.logger.debug(f"linear response put unit: {unit}")
        return unit
