import logging


class Strategy:
    def __init__(self, name: str, bet_strategy, put_strategy):
        self.name = name
        self.bet_strategy = bet_strategy
        self.put_strategy = put_strategy
        logging.debug(
            f"strategy initialized: {self.name}, put strategy: {self.put_strategy.name}, bet strategy: {self.bet_strategy.name}"
        )
