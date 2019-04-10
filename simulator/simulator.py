import threading
from collections import defaultdict, Counter

import pandas as pd
import yaml
from sqlalchemy import create_engine

from banker.banker import Banker
from config import constant as config_constant
from config.logger import get_logger
from player import constant as play_constant
from player.player import Player
from player.strategy_provider import StrategyProvider
from simulator import constant


class Simulator(object):
    def __init__(self, play_times, number_of_player, player_init_money, combination=1,
                 player_put_strategy=play_constant.linear_response, player_bet_strategy=play_constant.random,
                 to_db=False):

        with open('config/configuration.yml', 'r') as config:
            self.config = yaml.load(config)

        self.logger = get_logger(self.__class__.__name__)
        self.player_init_money = player_init_money
        self.banker = Banker(play_times=play_times)
        strategy_provider = StrategyProvider(self.config[config_constant.gambling][config_constant.ratio_per_game])
        self.players = self.init_players(player_put_strategy, player_bet_strategy, strategy_provider, number_of_player,
                                         play_times, combination)

        self.player_strategy = Counter(player_put_strategy)

        self.to_db = to_db
        if self.to_db:
            user = self.config[config_constant.DB][config_constant.user]
            password = self.config[config_constant.DB][config_constant.password]
            host = self.config[config_constant.DB][config_constant.host]
            self.engine = create_engine('mysql+pymysql://{}:{}@{}'.format(user, password, host))

    def init_players(self, player_put_strategy, player_bet_strategy, strategy_provider, number_of_players, play_times,
                     combination):
        player_bet_strategy = [player_bet_strategy] * number_of_players if isinstance(player_bet_strategy,
                                                                                      str) else player_bet_strategy
        player_put_strategy = [player_put_strategy] * number_of_players if isinstance(player_put_strategy,
                                                                                      str) else player_put_strategy

        return [Player(player_id=i, play_times=play_times, combination=combination, money=self.player_init_money,
                       put_strategy=put_strategy, bet_strategy=bet_strategy, strategy_provider=strategy_provider) for
                i, put_strategy, bet_strategy in
                zip(range(1, number_of_players + 1), player_put_strategy, player_bet_strategy)]

    def battle(self, player):
        self.logger.info('start battle with player: {}'.format(player.id))
        player.battle(self.banker.game_result)
        if self.to_db:
            self.write_to_db(player)

    def write_to_db(self, battled_player):
        self.logger.info('start write to db: {}'.format(self.config[config_constant.DB][config_constant.schema]))
        battled_player.battle_statistic.to_sql(con=self.engine, name='player_{}'.format(battled_player.id),
                                               if_exists='replace',
                                               schema=self.config[config_constant.DB][config_constant.schema],
                                               index_label='run')

        summarize_row = pd.DataFrame({k: v for k, v in battled_player.battle_summarize.items()}, index=[0])

        summarize_row.to_sql(con=self.engine, name=play_constant.player_summarize, if_exists='append',
                             schema=self.config[config_constant.DB][config_constant.schema], index=False)

    def start_simulation(self):
        self.logger.info('start simulation')
        battle_threads = []
        for player in self.players:
            battle_thread = threading.Thread(name=player.id, target=self.battle, args=(player,))
            battle_threads.append(battle_thread)
            battle_thread.start()

        for battle_thread in battle_threads:
            self.logger.info('join thread: {}'.format(battle_thread.getName()))
            battle_thread.join()

        self.logger.info('battle threads are finished')
        self.summarize_gambling()

    def summarize_gambling(self):
        self.logger.info('start summarize gambling')
        strategies = {k: defaultdict(int) for k in self.player_strategy.keys()}
        strategies['all'] = defaultdict(int)
        for player in self.players:
            strategies[player.strategy_name][constant.win_player_ratio] += (player.battle_summarize[
                play_constant.final_result]) / self.player_strategy[player.strategy_name]

            strategies[player.strategy_name][constant.average_player_win] += (player.battle_summarize[
                                                                                  play_constant.final_money] - self.player_init_money) / \
                                                                             self.player_strategy[player.strategy_name]

            strategies[player.strategy_name][constant.survival_player_ratio] += player.battle_summarize[
                                                                                    play_constant.still_survival] / \
                                                                                self.player_strategy[
                                                                                    player.strategy_name]

            strategies[player.strategy_name][constant.final_banker_money] += self.player_init_money - \
                                                                             player.battle_summarize[
                                                                                 play_constant.final_money]

            strategies[constant.all_strategy][constant.win_player_ratio] += (player.battle_summarize[
                play_constant.final_result]) / len(self.players)

            strategies[constant.all_strategy][constant.average_player_win] += (player.battle_summarize[
                                                                                   play_constant.final_money] - self.player_init_money) / len(
                self.players)

            strategies[constant.all_strategy][constant.survival_player_ratio] += player.battle_summarize[
                                                                                     play_constant.still_survival] / len(
                self.players)
            strategies[constant.all_strategy][constant.final_banker_money] += self.player_init_money - \
                                                                              player.battle_summarize[
                                                                                  play_constant.final_money]

        summarize_data = pd.DataFrame.from_dict(strategies).T
        summarize_data.insert(0, play_constant.put_strategy, summarize_data.index)
        summarize_data.reset_index(drop=True)

        self.logger.info('gambling summarize: {}'.format(summarize_data))
        if self.to_db:
            summarize_data.to_sql(con=self.engine, name=constant.gambling_summarize, if_exists='append',
                                  schema=self.config[config_constant.DB][config_constant.schema], index=False)
        return summarize_data
