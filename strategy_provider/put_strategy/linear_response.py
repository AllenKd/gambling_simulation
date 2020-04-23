from strategy_provider.common.base_put_strategy import BasePutStrategy


class LinearResponse(BasePutStrategy):
    def __init__(self):
        super().__init__("Linear Response")

    def get_unit(self, gambler, bet_strategy, **kwargs):
        assert kwargs["response_ratio"]
        unit = 1
        response = kwargs["response_ratio"]
        expect_response = response - unit
        put_accumulation = 0

        for d in gambler.decision_history[::-1]:
            if d.match:
                break
            else:
                put_accumulation += d.bet.unit
                expect_response += response - unit
                unit = (expect_response + put_accumulation) / (response - unit)
        self.logger.debug(f"linear response put unit: {unit}")
        return unit
