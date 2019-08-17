import functools
import threading

import pandas as pd
import pymysql
import yaml
from sqlalchemy import create_engine

from config.constant import database as db_constant
from config.constant import global_constant
from config.constant import player as player_constant
from config.constant import strategy_provider as sp_constant
from config.logger import get_logger
from player.player import Player
from strategy_provider.strategy import Strategy
from strategy_provider.strategy_provider import StrategyProvider


class Simulator(object):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml', 'r') as config:
            self.config = yaml.load(config, Loader=yaml.Loader)
        self.summarized_data = pd.DataFrame(columns=[sp_constant.bet_strategy] +
                                                    ['hit_ratio_{}'.format(col)
                                                     for col in player_constant.battle_target])
        self.players = None

        # init db
        user = self.config[global_constant.DB][global_constant.user]
        password = self.config[global_constant.DB][global_constant.password]
        host = self.config[global_constant.DB][global_constant.host]
        port = self.config[global_constant.DB][global_constant.port]
        self.db = pymysql.connect(host=host, user=user, passwd=password, port=port,
                                  db=self.config[global_constant.DB][global_constant.schema], charset='utf8')
        self.engine = create_engine('mysql+pymysql://{}:{}@{}:{}'.format(user, password, host, port))

    @functools.lru_cache(1)
    def init_players(self, num_of_player):
        self.logger.info('start init players')

        sp = StrategyProvider(battle_target=player_constant.battle_target)
        bet_strategy = [Strategy(sp_constant.keep_false, **dict()), Strategy(sp_constant.keep_true, **dict())]
        bet_strategy += [Strategy(sp_constant.random, **dict())] * ((num_of_player - 2) // 2)
        bet_strategy += [Strategy(sp_constant.low_of_large, **{'recency': i})
                         for i in range(1, num_of_player - len(bet_strategy) + 1)]
        self.players = [Player(player_id=i,
                               bet_strategy=bs,
                               strategy_provider=sp)
                        for i, bs in zip(range(1, num_of_player + 1), bet_strategy)]
        return self.players

    def start_simulation(self, num_of_player):
        self.logger.info('start simulation')
        game_judgement = pd.read_sql('SELECT id, {} FROM {}'.format(', '.join(player_constant.battle_target),
                                                                    db_constant.game_judgement),
                                     con=self.db,
                                     index_col=db_constant.row_id)
        battle_threads = []
        for player in self.init_players(num_of_player):
            battle_thread = threading.Thread(name=player.id, target=player.battle, args=(game_judgement,))
            battle_threads.append(battle_thread)
            battle_thread.start()
        for battle_thread in battle_threads:
            self.logger.debug('join thread: {}'.format(battle_thread.getName()))
            battle_thread.join()

        self.logger.info('battle threads are finished')

        self.write_to_db('battle_summarize', self.summarize_gambling(self.init_players(num_of_player)))

    def summarize_gambling(self, players):
        self.logger.info('start summarize gambling')
        for player in players:
            self.summarized_data.loc[player.id] = player.summarize_battle_history()
        return self.summarized_data

    def write_player_history_to_db(self):
        for player in self.players:
            self.write_to_db('player_{}'.format(player.id), player.battle_history)

    def write_to_db(self, table_name, df):
        self.logger.info('start write to db: {}'.format(table_name))
        df.to_sql(name=table_name,
                  if_exists='replace',
                  schema=self.config[global_constant.DB][global_constant.schema],
                  index_label='player_id',
                  con=self.engine)
