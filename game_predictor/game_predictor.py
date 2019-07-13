import pandas as pd
import pymysql
import yaml

from config.constant import database as db_constant
from config.constant import global_constant
from config.logger import get_logger


class GamePredictor(object):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)

        # create db connection
        user = self.config[global_constant.DB][global_constant.user]
        password = self.config[global_constant.DB][global_constant.password]
        host = self.config[global_constant.DB][global_constant.host]
        self.db = pymysql.connect(host=host, user=user, passwd=password,
                                  db=self.config[global_constant.DB][global_constant.schema], charset='utf8')

        self.raw_data = self.load_data()
        self.prepared_data = None
        self.logger.info('{} initialized'.format(self.__class__.__name__))

    def load_data(self):
        return pd.read_sql('SELECT * FROM {}'.format(db_constant.game_data), con=self.db, index_col=db_constant.game_id)

    def data_preparing(self):
        self.logger.info('start data preparing')
        guest_one_hot = pd.get_dummies(self.raw_data['guest'], prefix='guest')
        host_one_hot = pd.get_dummies(self.raw_data['host'], prefix='host')
        time_one_hot = pd.get_dummies(self.raw_data['play_time'], prefix='time')
        train_columns_from_game_data = [db_constant.national_host_point_spread,
                                        db_constant.national_total_point_threshold,
                                        db_constant.win_if_meet_spread_point, # information value equivalent to response_ratio_if_hit_spread_point
                                        db_constant.response_ratio_if_hit_spread_point,
                                        db_constant.local_host_point_spread,
                                        db_constant.local_host_point_spread_response_ratio,
                                        db_constant.local_total_point_threshold,
                                        db_constant.local_total_point_threshold_response_ratio]
        train_columns_from_prediction =

