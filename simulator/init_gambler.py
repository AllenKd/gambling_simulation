from strategy_provider.bet_strategy.anti_previous import AntiPrevious
from strategy_provider.bet_strategy.confidence_base import ConfidenceBase
from strategy_provider.bet_strategy.constant import Constant
from strategy_provider.bet_strategy.follow_previous import FollowPrevious
from strategy_provider.bet_strategy.low_response import LowResponse
from strategy_provider.bet_strategy.lowest_response import LowestResponse
from strategy_provider.bet_strategy.most_confidence import MostConfidence
from strategy_provider.put_strategy.constant import Constant as PutStrategyConstant
from strategy_provider.put_strategy.foo_double import FooDouble
from strategy_provider.put_strategy.kelly import Kelly
from strategy_provider.put_strategy.linear_response import LinearResponse
from gambler.gambler import Gambler
from db.collection.gambler import Gambler as GamblerCollection


def init_gamblers():
    # gamblers = [
    #     Gambler(name=i, principle=self.principle, strategy_provider=sp)
    #     for i, sp in enumerate(self.get_strategies())
    # ]

    gamblers = [
        Gambler(name=g.name, principle=g.principle, strategy_provider=sp)
        for g in GamblerCollection.objects
    ]

    for g in GamblerCollection.objects:
        pass

        gambler = Gambler(
            name=g.name,
            capital=g.capital,

        )


strategy_map = {
    "anti_previous": AntiPrevious,
    "confidence_base": ConfidenceBase,
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


def get_strategy(gambler):
    pass
