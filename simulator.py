import yaml
import pymysql
from player.player import Player
from banker.banker import Banker


class Simulator(object):
    def __init__(self, play_times, number_of_player, player_init_money, combination=1,
                 player_strategy='linear_response'):
        self.banker = Banker(play_times=play_times)
        self.players = [Player(player_id=i, play_times=play_times, combination=combination, money=player_init_money,
                               strategy=player_strategy) for i in range(1, number_of_player + 1)]

        with open('config/configuration.yml', 'r') as config:
            self.config = yaml.load(config)
            self.db = pymysql.connect(host=self.config['DB']['host'],
                                 user=self.config['DB']['user'],
                                 password=self.config['DB']['password'])

    def battle(self, player):
        player.battle(self.banker.game_result)
        battle_statistic = player.battle_statistic
        battle_statistic.to_sql(self.db)

    def start_simulation(self):
        pass



