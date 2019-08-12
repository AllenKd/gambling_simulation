import os

import math
import numpy as np
import pandas as pd
import yaml

from config.constant import global_constant
from config.constant import player as player_constant
from config.constant import strategy_provider as sp_constant
from config.logger import get_logger


class StrategyProvider(object):
    def __init__(self, ratio_per_game, bet_base=100, size=20):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)

        self.ratio_per_game = ratio_per_game
        self.bet_base = bet_base
        self.size = size

        linear = self.linear_response()
        fibonacci = self.fibonacci_base()
        foo_double = self.foo_double()
        self.strategy_table = linear.join(fibonacci).join(foo_double)

    def get_put_strategy(self, strategy, *args):
        self.logger.info('start get strategy: {}'.format(strategy))
        if strategy not in self.config[sp_constant.strategy_provider][sp_constant.put_strategy].keys():
            self.logger.warn('strategy: {} not in supporting strategy list'.format(strategy))
            return None

        if args not in self.config[sp_constant.strategy_provider][sp_constant.put_strategy][strategy]:
            self.logger.warn('given parameters of the strategy is not satisfied, required: {}, got: {}'.format(
                self.config[sp_constant.strategy_provider][sp_constant.put_strategy][strategy],
                args))
            return None

        if strategy == sp_constant.linear_response:
            pass

    def gen_linear_response(self, lose_count, ratio):
        pass
        return

    def all_strategy_table(self):
        return self.strategy_table

    def get_table_base_strategy(self, strategy_name, kind='unit'):
        flatten_columns = [' '.join(col).strip() for col in self.strategy_table.columns.values]
        selected_strategy = self.strategy_table.copy()
        selected_strategy.columns = flatten_columns
        if kind == 'unit':
            return selected_strategy.filter(regex='^{}.*unit$'.format(strategy_name))
        if kind == 'base':
            return selected_strategy.filter(
                items=[column for column in selected_strategy.columns if
                       not column.endswith('unit') and column.startswith(strategy_name)])
        if kind == 'all':
            return selected_strategy

    def get_residual_base_strategy(self, strategy_name, residual_chips=None):
        if strategy_name == player_constant.kelly:
            if residual_chips is None:
                self.logger.error('no residual chips specified')
                return 0

            self.logger.info('get kelly strategy')
            with open(os.path.abspath('__file__{}'.format('/../config/configuration.yml')), 'r') as config:
                config = yaml.load(config, Loader=yaml.Loader)
                return self.kelly_formula(chips=residual_chips,
                                          response_ratio=config[global_constant.gambling][
                                              global_constant.ratio_per_game],
                                          win_prob=1 / 2 ** config[global_constant.gambling][
                                              global_constant.combination])

    def linear_response(self):
        self.logger.info('start gen linear response table')
        expected_total_ratio = np.array([i * (self.ratio_per_game - 1) for i in range(1, self.size + 2)])
        expected_total = expected_total_ratio * self.bet_base

        bet_unit_list = [1]
        accumulative_put_list = [1]
        for i in range(self.size):
            bet_unit_list.append(self._get_current_put_unit(accumulative_put_list[-1], expected_total_ratio[i + 1]))
            accumulative_put_list.append(accumulative_put_list[-1] + bet_unit_list[-1])

        current_put_unit = np.array(bet_unit_list[:self.size])
        accumulative_put_unit = np.array(accumulative_put_list[:self.size])
        win_response_unit = current_put_unit * self.ratio_per_game
        subtotal_unit = win_response_unit - accumulative_put_unit

        current_put = current_put_unit * self.bet_base
        accumulative_put = accumulative_put_unit * self.bet_base
        win_response = current_put * self.ratio_per_game
        subtotal = win_response - accumulative_put

        strategy = pd.DataFrame({player_constant.expected_win_unit: expected_total_ratio[:self.size],
                                 player_constant.current_put_unit: current_put_unit,
                                 player_constant.accumulative_put_unit: accumulative_put_unit,
                                 player_constant.win_response_unit: win_response_unit,
                                 player_constant.subtotal_unit: subtotal_unit,
                                 player_constant.expected_win: expected_total[:self.size],
                                 player_constant.current_put: current_put,
                                 player_constant.accumulative_put: accumulative_put,
                                 player_constant.win_response: win_response,
                                 player_constant.subtotal: subtotal
                                 })

        columns = [np.array([player_constant.linear_response] * len(strategy.columns)),
                   strategy.columns]
        strategy.columns = columns
        return strategy

    def _get_current_put_unit(self, current_accumulative_put, current_expected_total_ratio):
        self.logger.info('start get current put unit: current accumulative put: {}, current expected total: {}'.format(
            current_accumulative_put, current_expected_total_ratio))
        cpu = math.ceil((current_expected_total_ratio + current_accumulative_put) / (self.ratio_per_game - 1))
        self.logger.info('the calculate result of current put unit: {}'.format(cpu))
        return cpu

    def fibonacci_base(self):
        current_put_unit = self._get_fib_array()
        return self._gen_strategy_table(current_put_unit, player_constant.fibonacci_base)

    def foo_double(self):
        current_put_unit = 2 ** np.arange(self.size)
        return self._gen_strategy_table(current_put_unit, player_constant.foo_double)

    def kelly_formula(self, chips, win_prob=0.5, response_ratio=None):
        # get optimized betting ratio
        response_ratio = self.ratio_per_game if not response_ratio else response_ratio
        bet_ratio = (win_prob * (response_ratio + 1) - 1) / response_ratio
        return round(bet_ratio * chips, -2)

    def _gen_strategy_table(self, current_put_unit, strategy_name):
        strategy = pd.DataFrame({player_constant.current_put_unit: current_put_unit,
                                 player_constant.accumulative_put_unit: np.cumsum(current_put_unit),
                                 player_constant.win_response_unit: current_put_unit * self.ratio_per_game,
                                 player_constant.subtotal_unit: current_put_unit * self.ratio_per_game - np.cumsum(
                                     current_put_unit),
                                 player_constant.current_put: current_put_unit * self.bet_base,
                                 player_constant.accumulative_put: np.cumsum(current_put_unit) * self.bet_base,
                                 player_constant.win_response: current_put_unit * self.ratio_per_game * self.bet_base,
                                 player_constant.subtotal: (current_put_unit * self.ratio_per_game - np.cumsum(
                                     current_put_unit)) * self.bet_base})
        columns = [np.array([strategy_name] * len(strategy.columns)),
                   strategy.columns]
        strategy.columns = columns
        return strategy

    def _get_fib_array(self):
        fibonacci_numbers = [0, 1]
        for i in range(2, self.size + 1):
            fibonacci_numbers.append(fibonacci_numbers[i - 1] + fibonacci_numbers[i - 2])
        return np.array(fibonacci_numbers[1:])
