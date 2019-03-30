import yaml
import threading
import pymysql
import pandas as pd
from player.player import Player
from player.strategy_provider import StrategyProvider
from banker.banker import Banker
from config.logger import get_logger
from sqlalchemy import create_engine
from collections import defaultdict, Counter


class Simulator(object):
    def __init__(self, play_times, number_of_player, player_init_money, combination=1,
                 player_strategy='linear_response', to_db=False):

        with open('config/configuration.yml', 'r') as config:
            self.config = yaml.load(config)

        self.logger = get_logger('simulator')
        self.player_init_money = player_init_money
        self.banker = Banker(play_times=play_times)
        strategy_provider = StrategyProvider(self.config['gambling']['ratio_per_game'])

        if isinstance(player_strategy, list):
            self.players = [Player(player_id=i, play_times=play_times, combination=combination, money=player_init_money,
                                   strategy_name=strategy, strategy_provider=strategy_provider) for i, strategy in
                            zip(range(1, number_of_player + 1), player_strategy)]
        elif isinstance(player_strategy, str):
            self.players = [Player(player_id=i, play_times=play_times, combination=combination, money=player_init_money,
                                   strategy_name=player_strategy, strategy_provider=strategy_provider) for i in
                            range(1, number_of_player + 1)]
            player_strategy = [player_strategy] * number_of_player
        else:
            self.logger.error('un-support strategy: {}'.format(player_strategy))
            return

        self.player_strategy = Counter(player_strategy)

        self.to_db = to_db
        if self.to_db:
            user = self.config['DB']['user']
            password = self.config['DB']['password']
            host = self.config['DB']['host']
            self.engine = create_engine('mysql+pymysql://{}:{}@{}'.format(user, password, host))
            self.engine.execute('CREATE SCHEMA IF NOT EXISTS {}'.format(self.config['DB']['schema']))
            self.db = pymysql.connect(host=host, user=user, passwd=password, db=self.config['DB']['schema'],
                                      charset='utf8')

    def battle(self, player):
        self.logger.info('start battle with player: {}'.format(player.id))
        player.battle(self.banker.game_result)
        if self.to_db:
            self.write_to_db(player)

    def write_to_db(self, battled_player):
        self.logger.info('start write to db: {}'.format(self.config['DB']['schema']))
        battled_player.battle_statistic.to_sql(con=self.engine, name='player_{}'.format(battled_player.id),
                                               if_exists='replace', schema=self.config['DB']['schema'],
                                               index_label='run')

        summarize_row = pd.DataFrame({k: v for k, v in battled_player.battle_summarize.items()}, index=[0])

        summarize_row.to_sql(con=self.engine, name='player_summarize', if_exists='append',
                             schema=self.config['DB']['schema'], index=False)

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
            strategies[player.strategy_name]['win_player_ratio'] += (player.battle_summarize['final_result']) / \
                                                                    self.player_strategy[player.strategy_name]
            strategies[player.strategy_name]['average_player_win'] += (player.battle_summarize[
                                                                           'final_money'] - self.player_init_money) / \
                                                                      self.player_strategy[player.strategy_name]
            strategies[player.strategy_name]['survival_player_ratio'] += player.battle_summarize['still_survival'] / \
                                                                         self.player_strategy[player.strategy_name]
            strategies[player.strategy_name]['final_banker_money'] += self.player_init_money - player.battle_summarize[
                'final_money']

            strategies['all']['win_player_ratio'] += (player.battle_summarize['final_result']) / len(self.players)
            strategies['all']['average_player_win'] += (player.battle_summarize[
                                                            'final_money'] - self.player_init_money) / len(self.players)
            strategies['all']['survival_player_ratio'] += player.battle_summarize['still_survival'] / len(self.players)
            strategies['all']['final_banker_money'] += self.player_init_money - player.battle_summarize['final_money']

        summarize_data = pd.DataFrame.from_dict(strategies).T
        summarize_data.insert(0, 'strategy', summarize_data.index)
        summarize_data.reset_index(drop=True)

        self.logger.info('gambling summarize: {}'.format(summarize_data))
        if self.to_db:
            summarize_data.to_sql(con=self.engine, name='gambling_summarize', if_exists='append',
                                  schema=self.config['DB']['schema'], index=False)
        return summarize_data
