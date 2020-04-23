from strategy_provider.common.base_put_strategy import BasePutStrategy


class FooDouble(BasePutStrategy):
    """
    Strategy Description:
        Double bet if lose, otherwise 1.

    Suitable Bet Strategies:
        One bet(decision) per day.
    """

    def __init__(self):
        super().__init__("Foo Double")

    def get_unit(self, gambler, base_strategy, **kwargs):
        unit = 1
        for r in gambler.decision_history[::-1]:
            if r.match:
                break
            else:
                unit *= 2
        return unit
