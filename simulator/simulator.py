import threading

from config.logger import get_logger
from gambler.gambler import Gambler
from strategy_provider.bet_strategy.anti_previous import AntiPrevious
from strategy_provider.bet_strategy.confidence_base import ConfidenceBaseBet
from strategy_provider.bet_strategy.constant import Constant
from strategy_provider.bet_strategy.follow_previous import FollowPrevious
from strategy_provider.bet_strategy.low_response import LowResponse
from strategy_provider.bet_strategy.lowest_response import LowestResponse
from strategy_provider.bet_strategy.most_confidence import MostConfidence
from strategy_provider.put_strategy.constant import Constant as PutStrategyConstant
from strategy_provider.put_strategy.foo_double import FooDouble
from strategy_provider.put_strategy.kelly import Kelly
from strategy_provider.put_strategy.linear_response import LinearResponse

from simulator.init_gambler import init_gamblers
import logging


class Simulator:
    def __init__(self):
        pass
    
    def start_simulation(self):
        logging.debug("start simulation")
        threads = []
        gamblers = init_gamblers()
        for g in gamblers:
            t = threading.Thread(target=g.n_battle, args=(self.start_date,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logging.debug(f"finished simulation, total gamblers: {len(gamblers)}")

    # def init_gamblers(self):
    #     logging.info("start init gamblers")
    #     gamblers = [
    #         Gambler(name=i, capital=self.principle, strategy=sp)
    #         for i, sp in enumerate(self.get_strategies())
    #     ]
    #     logging.debug(f"{len(gamblers)} gamblers initialized")
    #     return gamblers

    # Customize each strategies and parameters due to feature conflict between bet and put strategies.
    def get_strategies(self):
        return [
            Constant(put_strategy=PutStrategyConstant()),
            Constant(put_strategy=FooDouble()),
            Constant(put_strategy=LinearResponse()),
            ConfidenceBaseBet(
                put_strategy=PutStrategyConstant(), confidence_threshold=100
            ),
            ConfidenceBaseBet(
                put_strategy=PutStrategyConstant(), confidence_threshold=300
            ),
            ConfidenceBaseBet(
                put_strategy=PutStrategyConstant(), confidence_threshold=500
            ),
            ConfidenceBaseBet(
                put_strategy=PutStrategyConstant(), confidence_threshold=800
            ),
            ConfidenceBaseBet(put_strategy=Kelly(), confidence_threshold=100),
            ConfidenceBaseBet(put_strategy=Kelly(), confidence_threshold=300),
            ConfidenceBaseBet(put_strategy=Kelly(), confidence_threshold=500),
            ConfidenceBaseBet(put_strategy=Kelly(), confidence_threshold=800),
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
            LowResponse(put_strategy=PutStrategyConstant()),
            LowResponse(put_strategy=Kelly()),
            LowestResponse(put_strategy=PutStrategyConstant()),
            LowestResponse(put_strategy=FooDouble()),
            LowestResponse(put_strategy=LinearResponse()),
            LowestResponse(put_strategy=Kelly()),
            FollowPrevious(put_strategy=PutStrategyConstant()),
            FollowPrevious(put_strategy=FooDouble()),
            FollowPrevious(put_strategy=LinearResponse()),
            FollowPrevious(put_strategy=Kelly()),
            AntiPrevious(put_strategy=PutStrategyConstant()),
            AntiPrevious(put_strategy=FooDouble()),
            AntiPrevious(put_strategy=LinearResponse()),
            AntiPrevious(put_strategy=Kelly()),
        ]

    def summarize_gambling(self):
        logging.info("start summarize gambling")
        pass
