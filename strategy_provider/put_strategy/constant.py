from strategy_provider.common.base_put_strategy import BasePutStrategy


class Constant(BasePutStrategy):
    def __init__(self, unit):
        super().__init__("Constant")
        self.unit = unit

    def get_unit(self):
        return self.unit
