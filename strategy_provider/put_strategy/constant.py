from strategy_provider.common.base_put_strategy import BasePutStrategy


class Constant(BasePutStrategy):
    def __init__(self):
        super().__init__("Constant")

    def get_unit(self, gamble_info, decision, gambler, base_strategy, **kwargs):
        return kwargs.get("unit", 1)
