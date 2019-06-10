import numpy as np
import pandas as pd
import yaml

from config.constant import global_constant
from config.constant import player as player_constant
from config.logger import get_logger


class Player(object):
    def __init__(self, player_id, play_times, strategy_provider, combination=1, money=5000,
                 put_strategy='linear_response', bet_strategy=player_constant.random, bet_data=None):
        self.id = player_id
        self.logger = get_logger('player{}'.format(self.id))
        with open('config/configuration.yml', 'r') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)

        self.bet_strategy = bet_strategy
        if bet_data:
            self.bet_data = bet_data
        else:
            self.bet_data = None
            self._init_bet_data(play_times, combination)

        self.strategy_name = put_strategy

        # check if the strategy can be represent as a table
        if self.config[global_constant.support_strategy][self.strategy_name]:
            self.strategy = strategy_provider.get_table_base_strategy(strategy_name=put_strategy, kind='base')
            self.strategy.columns = [column.replace('{} '.format(put_strategy), '') for column in
                                     self.strategy.columns]
        else:
            self.strategy_provider = strategy_provider

        self.battle_statistic = pd.DataFrame(
            columns=[player_constant.current_put, player_constant.win_result, player_constant.current_response,
                     player_constant.subtotal])
        self.money = money
        self.final_money = money
        self.battle_result = None
        self.battle_summarize = None
        self.max_continuous_lost_count = 0

        self.logger.info('strategy: {}, initial money: {}'.format(put_strategy, self.money))

    def _init_bet_data(self, play_times, combination):
        if self.bet_strategy == player_constant.random:
            self.bet_data = np.random.randint(2, size=play_times * combination).reshape(play_times, combination)

        if self.bet_strategy == player_constant.keep_false:
            self.bet_data = np.zeros((play_times, 1), dtype=int)

        if self.bet_strategy == player_constant.keep_true:
            self.bet_data = np.ones((play_times, 1), dtype=int)

        if self.bet_strategy == player_constant.follow_last:
            # the bet strategy cannot be determine at this stage
            self.bet_data = None

    def battle(self, banker_result):
        self.logger.info('start battle'.format(self.id))
        if self.bet_data is None:
            self.logger.info('prepare bet data for bet strategy: {}'.format(self.bet_strategy))
            self._prepare_bet_data(banker_result)
        self.battle_result = self.bet_data == banker_result
        self.logger.debug('player battle result: {}, win ratio: {}'.format(self.battle_result,
                                                                           np.sum(self.battle_result) / len(
                                                                               self.bet_data)))
        self._gen_battle_statistic_table()
        return self.battle_result

    def _prepare_bet_data(self, banker_result):
        if self.bet_strategy == player_constant.follow_last:
            self.logger.debug('generate bet data for strategy: {}'.format(self.bet_strategy))
            self.bet_data = np.roll(banker_result, 1)

    def _gen_battle_statistic_table(self):
        self.logger.info('start generate battle statistic table')

        if self.battle_result is None:
            self.logger.error('not battle yet, have to perform battle first')
            return

        lose_count = 0
        for run, single_result in enumerate(self.battle_result):
            single_result = single_result[0]
            current_put = self.strategy[player_constant.current_put].iloc[lose_count] if \
                self.config[global_constant.support_strategy][
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
                current_response = current_put * self.config[global_constant.gambling][global_constant.ratio_per_game]
            else:
                self.logger.info('lose {}th game'.format(run))
                lose_count += 1
                self.max_continuous_lost_count = max(lose_count, self.max_continuous_lost_count)
                current_response = 0

            self.final_money += current_response
            self.logger.info('subtotal of {}th run: {}'.format(run, self.final_money))
            self.battle_statistic.loc[run] = {player_constant.current_put: int(current_put),
                                              player_constant.win_result: single_result,
                                              player_constant.current_response: int(current_response),
                                              player_constant.subtotal: int(self.final_money)}

        self.battle_statistic[player_constant.actual_win] = self.battle_statistic['subtotal'] - self.money
        self.battle_statistic[player_constant.expected_win] = np.array(
            [int((self.config[global_constant.gambling][global_constant.ratio_per_game] - 1) *
                 self.config[global_constant.gambling][global_constant.bet_base] * i) for i in
             range(1, len(self.battle_statistic.index) + 1)])

        self.summarize()

    def summarize(self):
        self.logger.info('summarize battle result')
        self.battle_summarize = {player_constant.player_id: self.id,
                                 player_constant.put_strategy: self.strategy_name,
                                 player_constant.bet_strategy: self.bet_strategy,
                                 player_constant.initial_money: self.money,
                                 player_constant.still_survival: len(self.battle_statistic.index) == len(self.bet_data),
                                 player_constant.win_ratio: (sum(self.battle_result) / len(self.battle_result))[0],
                                 player_constant.max_continuous_lose_count: self.max_continuous_lost_count,
                                 player_constant.final_money: self.final_money,
                                 player_constant.final_result: bool(self.final_money > self.money)}
