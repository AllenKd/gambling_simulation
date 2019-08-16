import functools
import math

import numpy as np
import yaml

from config.constant import global_constant
from config.constant import strategy_provider as sp_constant
from config.logger import get_logger


class StrategyProvider(object):
    def __init__(self, battle_target):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)

        self.battle_target = battle_target

    @functools.lru_cache(16)
    def get_put_unit(self, put_strategy, *args):
        self.logger.info('start get strategy: {}'.format(put_strategy))
        if put_strategy not in self.config[sp_constant.strategy_provider][sp_constant.put_strategy].keys():
            self.logger.warn('strategy: {} not in supporting strategy list'.format(put_strategy))
            return None

        if args not in self.config[sp_constant.strategy_provider][sp_constant.put_strategy][put_strategy]:
            self.logger.warn('given parameters of the strategy is not satisfied, required: {}, got: {}'.format(
                self.config[sp_constant.strategy_provider][sp_constant.put_strategy][put_strategy], args))
            return None

        if put_strategy == sp_constant.linear_response:
            self.gen_linear_response(*args)

        if put_strategy == sp_constant.fibonacci_base:
            # return ith fibonacci number
            return (np.power([1 + math.sqrt(len(self.battle_target))] * len(self.battle_target), args[0]) -
                    np.power([1 - math.sqrt(len(self.battle_target))] * len(self.battle_target), args[0])) / \
                   (np.power([2] * len(self.battle_target), args[0]) * math.sqrt(len(self.battle_target)))

        if put_strategy == sp_constant.foo_double:
            return np.power([2] * len(self.battle_target), args[0])

        if put_strategy == sp_constant.kelly:
            return self.kelly_formula(*args)

        if put_strategy == sp_constant.constant:
            return np.array([1] * len(self.battle_target))

    # get amount of put unit at current gamble
    @functools.lru_cache(16)
    def gen_linear_response(self, lose_count, ratio):
        # if lose_count == 0:
        #     return 1
        # if lose_count == 1:
        # cpu = math.ceil((current_expected_total_ratio + current_accumulative_put) / (self.ratio_per_game - 1))
        # return math.ceil(lose_count / ratio)
        # expected = 1 + (ratio - 1) * lose_count

        return (1 + lose_count) * lose_count / 2

    def get_bet_decision(self, bet_strategy, **kwargs):
        self.logger.info('start get bet decision: {}'.format(bet_strategy.name))
        if bet_strategy.name not in self.config[sp_constant.strategy_provider][sp_constant.bet_strategy].keys():
            self.logger.warn('strategy: {} not in supporting strategy list'.format(bet_strategy.name))
            return None
        if list(kwargs.keys()) != self.config[sp_constant.strategy_provider][sp_constant.bet_strategy][bet_strategy.name]:
            self.logger.warn('given parameters of the strategy is not satisfied, required: {}, got: {}'.format(
                self.config[sp_constant.strategy_provider][sp_constant.bet_strategy][bet_strategy.name], kwargs.keys()))
            return None

        if bet_strategy.name == sp_constant.random:
            return np.random.randint(2, size=len(self.battle_target))

        if bet_strategy.name == sp_constant.keep_true:
            return np.array([1] * len(self.battle_target))

        if bet_strategy.name == sp_constant.keep_false:
            return np.array([0] * len(self.battle_target))

        if bet_strategy.name == sp_constant.low_of_large:
            if len(kwargs['game_history']) > 0:
                return np.where(np.rint(kwargs['game_history'].tail(bet_strategy.kwargs['recency']).mean()) > 0.5, 0, 1)
            else:
                return np.random.randint(2, size=len(self.battle_target))

    def kelly_formula(self, remaining_unit, win_prob=0.5, response_ratio=None):
        response_ratio = self.config[global_constant.gambling][global_constant.ratio_per_game] if not response_ratio \
            else response_ratio
        bet_ratio = (win_prob * (response_ratio + 1) - 1) / response_ratio
        return np.array([round(bet_ratio * remaining_unit, 0)] * self.battle_target)
