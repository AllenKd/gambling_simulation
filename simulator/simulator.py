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

        # [(strategy, [{parameter: value, ...}, ...]), ...]
        self.bet_strategies = [
            (Constant, [{}]),
            (
                ConfidenceBase,
                [
                    {"confidence_threshold": 100},
                    {"confidence_threshold": 300},
                    {"confidence_threshold": 500},
                    {"confidence_threshold": 800},
                ],
            ),
            (
                MostConfidence,
                [
                    {"confidence_threshold": 100},
                    {"confidence_threshold": 300},
                    {"confidence_threshold": 500},
                    {"confidence_threshold": 800},
                ],
            ),
        ]
        self.put_strategies = [
            (PutStrategyConstant, [{}]),
            (FooDouble, [{}]),
            (LinearResponse, [{}]),
            (Kelly, [{}]),
        ]

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

    # Get strategies based on the combination of bet_strategy, put_strategy and each parameters
    def get_strategies(self):
        strategies = []
        for bet_strategy, bet_parameters in self.bet_strategies:
            for put_strategy, put_parameters in self.put_strategies:
                strategies += [
                    self.init_strategy(bet_strategy, put_strategy, bp, pp)
                    for bp in bet_parameters
                    for pp in put_parameters
                ]
        return strategies

    def init_strategy(self, bet_strategy, put_strategy, bet_parameter, put_parameter):
        ps = put_strategy(**put_parameter) if put_parameter else put_strategy()
        bs = bet_strategy(ps, **bet_parameter) if bet_parameter else bet_strategy(ps)
        return bs

    def summarize_gambling(self):
        self.logger.info("start summarize gambling")
        pass
