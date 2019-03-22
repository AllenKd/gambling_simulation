import yaml
import threading
import pymysql
import pandas as pd
from player import Player
from banker import Banker
from config.logger import get_logger
from sqlalchemy import create_engine


class Simulator(object):
    def __init__(self, play_times, number_of_player, player_init_money, combination=1,
                 player_strategy='linear_response', to_db=False):
        self.logger = get_logger('simulator')
        self.banker = Banker(play_times=play_times)
        self.players = [Player(player_id=i, play_times=play_times, combination=combination, money=player_init_money,
                               strategy=player_strategy) for i in range(1, number_of_player + 1)]

        self.to_db = to_db
        if self.to_db:
            with open('config/configuration.yml', 'r') as config:
                self.config = yaml.load(config)
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
        for player in self.players:
            threading.Thread(target=self.battle, args=(player,)).start()


if __name__ == '__main__':
    times = 100
    a = Simulator(play_times=times, number_of_player=10, player_init_money=10000, to_db=True)
    a.start_simulation()
