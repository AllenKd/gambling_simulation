import numpy as np
import pandas as pd
import yaml
import os
from config.logger import get_logger


class Player(object):
    def __init__(self, player_id, play_times, strategy_provider, combination=1, money=5000,
                 strategy_name='linear_response'):
        self.id = player_id
        self.logger = get_logger('player{}'.format(self.id))
        with open(os.path.abspath('__file__{}'.format('/../config/configuration.yml')), 'r') as config:
            self.config = yaml.load(config)
        self.bet_data = np.random.randint(2, size=play_times * combination).reshape(play_times, combination)
        self.strategy_name = strategy_name

        # check if the strategy can be represent as a table
        if self.config['support_strategy'][self.strategy_name]:
            self.strategy = strategy_provider.get_table_base_strategy(strategy_name=strategy_name, kind='base')
            self.strategy.columns = [column.replace('{} '.format(strategy_name), '') for column in
                                     self.strategy.columns]
        else:
            self.strategy_provider = strategy_provider

        self.battle_statistic = pd.DataFrame(columns=['current_put', 'win_result', 'current_response', 'subtotal'])
        self.money = money
        self.final_money = money
        self.battle_result = None
        self.battle_summarize = None
        self.max_continuous_lost_count = 0

        self.logger.info('strategy: {}, initial money: {}'.format(strategy_name, self.money))

    def battle(self, banker_result):
        self.logger.info('start battle'.format(self.id))
        self.battle_result = self.bet_data == banker_result
        self.logger.debug('player battle result: {}, win ratio: {}'.format(self.battle_result,
                                                                           np.sum(self.battle_result) / len(
                                                                               self.bet_data)))
        self._gen_battle_statistic_table()
        return self.battle_result

    def _gen_battle_statistic_table(self):
        self.logger.info('start generate battle statistic table')

        if self.battle_result is None:
            self.logger.error('not battle yet, have to perform battle first')
            return

        lose_count = 0
        for run, single_result in enumerate(self.battle_result):
            single_result = single_result[0]
            current_put = self.strategy['current_put'].iloc[lose_count] if self.config['support_strategy'][
                self.strategy_name] else self.strategy_provider.get_residual_base_strategy(self.strategy_name,
                                                                                           self.final_money)
            self.logger.info('put {} at {} run'.format(current_put, run))
            self.final_money -= current_put
            if self.final_money < 0:
                self.final_money += current_put
                self.logger.info('no money to bet, out'.format(self.id))
                break

            if single_result:
                self.logger.info('wins {}th game'.format(run))
                lose_count = 0
                current_response = current_put * self.config['gambling']['ratio_per_game']
            else:
                self.logger.info('lose {}th game'.format(run))
                lose_count += 1
                self.max_continuous_lost_count = max(lose_count, self.max_continuous_lost_count)
                current_response = 0

            self.final_money += current_response
            self.logger.info('subtotal of {}th run: {}'.format(run, self.final_money))
            self.battle_statistic.loc[run] = {'current_put': int(current_put),
                                              'win_result': single_result,
                                              'current_response': int(current_response),
                                              'subtotal': int(self.final_money)}

        self.battle_statistic['actual_win'] = self.battle_statistic['subtotal'] - self.money
        self.battle_statistic['expected_win'] = np.array(
            [int((self.config['gambling']['ratio_per_game'] - 1) * self.config['gambling']['bet_base'] * i) for i in
             range(1, len(self.battle_statistic.index) + 1)])

        self.summarize()

    def summarize(self):
        self.logger.info('summarize battle result')
        self.battle_summarize = {'player_id': self.id,
                                 'strategy': self.strategy_name,
                                 'initial money': self.money,
                                 'still_survival': len(self.battle_statistic.index) == len(self.bet_data),
                                 'win_ratio': (sum(self.battle_result) / len(self.battle_result))[0],
                                 'max_continuous_lose_count': self.max_continuous_lost_count,
                                 'final_money': self.final_money,
                                 'final_result': bool(self.final_money > self.money)}
