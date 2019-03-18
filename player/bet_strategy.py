import numpy as np
import math
import pandas as pd
from config.logger import get_logger


class StrategyProvider(object):
    def __init__(self, ratio_per_game, bet_base=100, size=20):
        self.ratio_per_game = ratio_per_game
        self.bet_base = bet_base
        self.size = size
        self.logger = get_logger(0)

        linear = self.linear_response()
        fibonacci = self.fibonacci_base()
        foo_double = self.foo_double()
        self.strategy_table = linear.join(fibonacci).join(foo_double)

    def all_strategy_table(self):
        return self.strategy_table

    def get_strategy(self, strategy_name, kind='unit'):
        flatten_columns = [' '.join(col).strip() for col in self.strategy_table.columns.values]
        selected_strategy = self.strategy_table
        selected_strategy.columns = flatten_columns
        if kind == 'unit':
            return selected_strategy.filter(regex='^{}.*unit$'.format(strategy_name))
        if kind == 'base':
            return selected_strategy.filter(
                items=[column for column in selected_strategy.columns if
                       not column.endswith('unit') and column.startswith(strategy_name)])
        if kind == 'all':
            return selected_strategy

    def linear_response(self):
        self.logger.info('start gen linear response table')
        expected_total_ratio = np.array([i * (self.ratio_per_game - 1) for i in range(1, self.size + 1)])
        expected_total = expected_total_ratio * self.bet_base

        bet_unit_list = []
        accumulative_put_list = [0]
        for i in range(self.size):
            bet_unit_list.append(self._get_current_put_unit(accumulative_put_list[-1], expected_total_ratio[i]))
            accumulative_put_list.append(accumulative_put_list[-1] + bet_unit_list[-1])

        current_put_unit = np.array(bet_unit_list[:self.size])
        accumulative_put_unit = np.array(accumulative_put_list[:self.size])
        win_response_unit = current_put_unit * self.ratio_per_game
        subtotal_unit = win_response_unit - accumulative_put_unit - current_put_unit

        current_put = current_put_unit * self.bet_base
        accumulative_put = accumulative_put_unit * self.bet_base
        win_response = current_put * self.ratio_per_game
        subtotal = win_response - accumulative_put

        strategy = pd.DataFrame({'expected_win_unit': expected_total_ratio,
                                 'current_put_unit': current_put_unit,
                                 'accumulative_put_unit': accumulative_put_unit,
                                 'win_response_unit': win_response_unit,
                                 'subtotal_unit': subtotal_unit,
                                 'expected_win': expected_total,
                                 'current_put': current_put,
                                 'accumulative_put': accumulative_put,
                                 'win_response': win_response,
                                 'subtotal': subtotal
                                 })

        columns = [np.array(['linear_response'] * len(strategy.columns)),
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
        return self._gen_strategy_table(current_put_unit, 'fibonacci_base')

    def foo_double(self):
        current_put_unit = 2 ** np.arange(self.size)
        return self._gen_strategy_table(current_put_unit, 'foo_double')

    def kelly_formula(self, win_prob=0.5, response_ratio=None):
        # get optimized betting ratio
        response_ratio = self.ratio_per_game if not response_ratio else response_ratio

        return (win_prob * (response_ratio + 1) - 1) / response_ratio

    def _gen_strategy_table(self, current_put_unit, strategy_name):
        strategy = pd.DataFrame({'current_put_unit': current_put_unit,
                                 'accumulative_put_unit': np.cumsum(current_put_unit),
                                 'win_response_unit': current_put_unit * self.ratio_per_game,
                                 'subtotal_unit': current_put_unit * self.ratio_per_game - np.cumsum(current_put_unit),
                                 'current_put': current_put_unit * self.bet_base,
                                 'accumulative_put': np.cumsum(current_put_unit) * self.bet_base,
                                 'win_response': current_put_unit * self.ratio_per_game * self.bet_base,
                                 'subtotal': (current_put_unit * self.ratio_per_game - np.cumsum(
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


if __name__ == '__main__':
    import yaml

    with open('../config/configuration.yml', 'r') as config:
        c = yaml.load(config)
    a = StrategyProvider(1.75)
    d = a.get_strategy(c['support_strategy'][0], kind='base')
    print(d)
