import pytest

from gambler.gambler import Gambler
from strategy_provider.common.decision import Decision, Bet
from strategy_provider.put_strategy.constant import Constant
from strategy_provider.put_strategy.foo_double import FooDouble
from strategy_provider.put_strategy.linear_response import LinearResponse


@pytest.fixture(scope="class")
def setup_test_data():
    return Gambler(name=-1, capital=-1, strategy_provider=None)


def init_gamble_hist(match_hist, bet_list=None):
    gamble_hist = [Decision(None, None, None, None) for _ in match_hist]
    for h, m in zip(gamble_hist, match_hist):
        h.match = m

    if bet_list:
        for h, b in zip(gamble_hist, bet_list):
            h.bet = b
    return gamble_hist


class TestPutStrategy:
    def test_constant(self):
        g = Gambler(name=-1, capital=-1, strategy_provider=None)
        c = Constant()
        assert c.get_unit(g, None) == 1

        for i in range(10):
            assert c.get_unit(g, None, unit=i) == i

    def test_foo_double(self):
        g = Gambler(name=-1, capital=-1, strategy_provider=None)

        for i in range(1, 8):
            match_hist = [False] * i
            g.decision_history = init_gamble_hist(match_hist)
            assert FooDouble().get_unit(g, None) == 2 ** i

            match_hist = [True] * i
            g.decision_history = init_gamble_hist(match_hist)
            assert FooDouble().get_unit(g, None) == 1

    def test_linear_response(self):
        g = Gambler(name=-1, capital=-1, strategy_provider=None)
        u = 1
        bet_list = [Bet(None, None, None, 1)]
        for i in range(1, 15):
            match_list = [False] * i
            bet_list += [Bet(None, None, None, u)]
            g.decision_history = init_gamble_hist(match_list, bet_list)
            r = 1.75
            u = LinearResponse().get_unit(g, None, response=r)
            assert u * (r - 1) >= (r - 1) * (len(bet_list) + 1)
