import multiprocessing

from config.logger import get_logger
from gambler.gambler import Gambler
from strategy_provider.bet_strategy.confidence_base import ConfidenceBase
from strategy_provider.bet_strategy.constant import Constant
from strategy_provider.bet_strategy.most_confidence import MostConfidence
from strategy_provider.put_strategy.constant import Constant as PutStrategyConstant
from strategy_provider.put_strategy.foo_double import FooDouble
from strategy_provider.put_strategy.kelly import Kelly
from strategy_provider.put_strategy.linear_response import LinearResponse


class Simulator:
    def __init__(self, principle=100, start_date="20180929"):
        self.logger = get_logger(self.__class__.__name__)

        self.principle = principle
        self.start_date = start_date

    def start_simulation(self):
        self.logger.debug("start simulation")
        processes = []
        for g in self.init_gamblers():
            p = multiprocessing.Process(target=g.battle, args=(self.start_date,))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        self.logger.debug("finished simulation")

    def init_gamblers(self):
        self.logger.info("start init gamblers")
        gamblers = [
            Gambler(gambler_id=i, principle=self.principle, strategy_provider=sp)
            for i, sp in enumerate(self.get_strategies())
        ]
        self.logger.debug(f"{len(gamblers)} gamblers initialized")
        return gamblers

    # Customize each strategies and parameters due to feature conflict between bet and put strategies.
    def get_strategies(self):
        return [
            Constant(put_strategy=PutStrategyConstant()),
            Constant(put_strategy=FooDouble()),
            Constant(put_strategy=LinearResponse()),
            ConfidenceBase(
                put_strategy=PutStrategyConstant(), confidence_threshold=100
            ),
            ConfidenceBase(
                put_strategy=PutStrategyConstant(), confidence_threshold=300
            ),
            ConfidenceBase(
                put_strategy=PutStrategyConstant(), confidence_threshold=500
            ),
            ConfidenceBase(
                put_strategy=PutStrategyConstant(), confidence_threshold=800
            ),
            ConfidenceBase(put_strategy=FooDouble(), confidence_threshold=100),
            ConfidenceBase(put_strategy=FooDouble(), confidence_threshold=300),
            ConfidenceBase(put_strategy=FooDouble(), confidence_threshold=500),
            ConfidenceBase(put_strategy=FooDouble(), confidence_threshold=800),
            ConfidenceBase(put_strategy=LinearResponse(), confidence_threshold=100),
            ConfidenceBase(put_strategy=LinearResponse(), confidence_threshold=300),
            ConfidenceBase(put_strategy=LinearResponse(), confidence_threshold=500),
            ConfidenceBase(put_strategy=LinearResponse(), confidence_threshold=800),
            ConfidenceBase(put_strategy=Kelly(), confidence_threshold=100),
            ConfidenceBase(put_strategy=Kelly(), confidence_threshold=300),
            ConfidenceBase(put_strategy=Kelly(), confidence_threshold=500),
            ConfidenceBase(put_strategy=Kelly(), confidence_threshold=800),
            MostConfidence(
                put_strategy=PutStrategyConstant(), confidence_threshold=100
            ),
            MostConfidence(
                put_strategy=PutStrategyConstant(), confidence_threshold=300
            ),
            MostConfidence(
                put_strategy=PutStrategyConstant(), confidence_threshold=500
            ),
            MostConfidence(
                put_strategy=PutStrategyConstant(), confidence_threshold=800
            ),
            MostConfidence(put_strategy=FooDouble(), confidence_threshold=100),
            MostConfidence(put_strategy=FooDouble(), confidence_threshold=300),
            MostConfidence(put_strategy=FooDouble(), confidence_threshold=500),
            MostConfidence(put_strategy=FooDouble(), confidence_threshold=800),
            MostConfidence(put_strategy=LinearResponse(), confidence_threshold=100),
            MostConfidence(put_strategy=LinearResponse(), confidence_threshold=300),
            MostConfidence(put_strategy=LinearResponse(), confidence_threshold=500),
            MostConfidence(put_strategy=LinearResponse(), confidence_threshold=800),
            MostConfidence(put_strategy=Kelly(), confidence_threshold=100),
            MostConfidence(put_strategy=Kelly(), confidence_threshold=300),
            MostConfidence(put_strategy=Kelly(), confidence_threshold=500),
            MostConfidence(put_strategy=Kelly(), confidence_threshold=800),
        ]

    def summarize_gambling(self):
        self.logger.info("start summarize gambling")
        pass
