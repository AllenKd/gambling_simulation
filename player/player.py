import numpy as np
import pandas as pd
import yaml
from config.logger import get_logger
from bet_strategy import StrategyProvider


class Player(object):
    def __init__(self, player_id, play_times, combination=1, money=5000, strategy='linear_response'):
        self.id = player_id
        self.logger = get_logger(self.id)
        self.bet_data = np.random.randint(2, size=play_times * combination).reshape(play_times, combination)
        self.strategy = StrategyProvider(1.75).get_strategy(strategy_name=strategy, kind='base')
        self.strategy.columns = [column.replace('{} '.format(strategy), '') for column in self.strategy.columns]
        self.battle_statistic = pd.DataFrame(columns=['current_put', 'win_result', 'current_response', 'subtotal'])
        self.money = money
        self.final_money = money
        self.battle_result = None
        self.battle_summarize = None
        self.max_continuous_lost_count = 0

        with open('../config/configuration.yml', 'r') as config:
            self.config = yaml.load(config)

        self.logger.info('player {}, strategy: {}, initial money: {}'.format(self.id, self.strategy, self.money))

    def battle(self, banker_result):
        self.logger.info('player {} start battle'.format(self.id))
        self.battle_result = self.bet_data == banker_result
        self.logger.debug('player battle result: {}, win ratio: {}'.format(self.battle_result,
                                                                           np.sum(self.battle_result) / len(
                                                                               self.battle_result)))
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
            current_put = self.strategy['current_put'].iloc[lose_count]
            self.logger.info('player {} put {} at {} run'.format(self.id, current_put, run))
            self.final_money -= current_put
            if self.final_money < 0:
                self.logger.info('player {} no money to bet, out'.format(self.id))
                break

            if single_result:
                self.logger.info('player {} wins {}th game'.format(self.id, run))
                lose_count = 0
                current_response = current_put * self.config['ratio_per_game']
            else:
                self.logger.info('player {} lose {}th game'.format(self.id, run))
                lose_count += 1
                self.max_continuous_lost_count = max(lose_count, self.max_continuous_lost_count)
                current_response = 0

            self.final_money += current_response
            self.logger.info('player {} subtotal of {}th run: {}'.format(self.id, run, self.final_money))
            self.battle_statistic.loc[run] = {'current_put': int(current_put),
                                              'win_result': single_result,
                                              'current_response': int(current_response),
                                              'subtotal': int(self.final_money)}

        self.battle_statistic['actual_win'] = self.battle_statistic['subtotal'] - self.money
        self.battle_statistic['expected_win'] = np.array(
            [int((self.config['ratio_per_game'] - 1) * self.config['bet_base'] * i) for i in
             range(1, len(self.battle_statistic.index) + 1)])

    def summarize(self):
        self.battle_summarize = {'still_survival': len(self.battle_statistic.index) == len(self.bet_data),
                                 'win_ratio': sum(self.battle_result) / len(self.battle_result),
                                 'max_continuous_lose_count': self.max_continuous_lost_count,
                                 'final_money': self.final_money,
                                 'final_result': self.final_money > self.money}


if __name__ == '__main__':
    times = 100
    a = Player(player_id=0, play_times=times, combination=1, money=10000)
    banker_result = np.random.randint(2, size=times).reshape(times, 1)
    a.battle(banker_result)
    print(a.battle_statistic)
