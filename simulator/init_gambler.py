import logging

from db.collection.gambler import Gambler as GamblerCollection
from gambler.gambler import Gambler
from strategy_provider.bet_strategy.anti_previous import AntiPrevious
from strategy_provider.bet_strategy.confidence_base import ConfidenceBaseBet
from strategy_provider.bet_strategy.constant import Constant
from strategy_provider.bet_strategy.follow_previous import FollowPrevious
from strategy_provider.bet_strategy.lowest_response import LowestResponse
from strategy_provider.bet_strategy.most_confidence import MostConfidence
from strategy_provider.common.base_strategy import Strategy
from strategy_provider.put_strategy.constant import Constant as PutStrategyConstant
from strategy_provider.put_strategy.foo_double import FooDouble
from strategy_provider.put_strategy.kelly import Kelly
from strategy_provider.put_strategy.linear_response import LinearResponse


def init_gamblers() -> [Gambler]:
    gamblers = []
    for g in GamblerCollection.objects:
        logging.debug(f"init gambler: {g}")
        try:
            strategy = parse_strategy(g.strategy)
            gambler = Gambler(name=g.name, capital=g.capital, strategy=strategy)
            gamblers.append(gambler)
        except Exception as e:
            logging.error(e)

    return gamblers


bet_strategy_map = {
    "anti_previous": AntiPrevious,
    "confidence_base": ConfidenceBaseBet,
    "constant": Constant,
    "follow_previous": FollowPrevious,
    "lowest_response": LowestResponse,
    "most_confidence": MostConfidence,
}
put_strategy_map = {
    "constant": PutStrategyConstant,
    "foo_double": FooDouble,
    "kelly": Kelly,
    "linear_response": LinearResponse,
}


def parse_strategy(strategy: GamblerCollection.strategy) -> Strategy:
    if strategy.bet.name not in bet_strategy_map:
        raise Exception(f"invalid bet strategy: {strategy.bet.name}")
    if strategy.put.name not in put_strategy_map:
        raise Exception(f"invalid put strategy: {strategy.put.name}")

    return Strategy(
        name=strategy.name,
        bet_strategy=bet_strategy_map[strategy.bet.name](**strategy.bet.parameters),
        put_strategy=put_strategy_map[strategy.put.name](**strategy.put.parameters),
    )
