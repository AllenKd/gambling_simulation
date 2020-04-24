import math

from strategy_provider.common.base_put_strategy import BasePutStrategy


class LinearResponse(BasePutStrategy):
    def __init__(self):
        super().__init__("Linear Response")

    def get_unit(self, gambler, bet_strategy, **kwargs):
        assert kwargs["response"]
        unit = 1
        response = kwargs["response"]
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
