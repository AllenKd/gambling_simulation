import yaml
import pymysql
import pandas as pd
from sqlalchemy import create_engine

from config import constant as config_constant
from config.logger import get_logger
from crawler import constant as crawler_constant
from database import constant as db_constant
from analysis import constant as analysis_constant


class CrawledResultAnalyzer(object):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)

            # init db
            user = self.config[config_constant.DB][config_constant.user]
            password = self.config[config_constant.DB][config_constant.password]
            host = self.config[config_constant.DB][config_constant.host]
            self.engine = create_engine('mysql+pymysql://{}:{}@{}'.format(user, password, host))
            self.db = pymysql.connect(host=host, user=user, passwd=password,
                                      db=self.config[config_constant.DB][config_constant.schema], charset='utf8')

        self.judgement = None

    def start_analyzer(self):
        a = self.get_game_data()
        self.judge(a)

    def get_game_data(self, start_date=None, total_date=None, end_date=None):
        return pd.read_sql('SELECT * FROM {}'.format(db_constant.game_data), con=self.db, index_col=db_constant.game_id)

    def judge(self, game_data):
        self.logger.info('start game result judge')

        self.judgement = pd.DataFrame(index=game_data.index)

        self.judgement[analysis_constant.win_original] = \
            game_data[db_constant.guest_score] < game_data[db_constant.host_score]

        self.judgement[analysis_constant.host_win_point_spread_national] = game_data[db_constant.guest_score] < (
                game_data[db_constant.host_score] - game_data[db_constant.national_host_point_spread])

        self.judgement[analysis_constant.host_win_point_spread_local] = game_data[db_constant.guest_score] < (
                game_data[db_constant.host_score] - game_data[db_constant.local_host_point_spread])

        self.judgement[analysis_constant.over_total_point_national] = (game_data[db_constant.guest_score] + game_data[
            db_constant.host_score]) > game_data[db_constant.national_total_point_threshold]

        self.judgement[analysis_constant.over_total_point_local] = (game_data[db_constant.guest_score] + game_data[
            db_constant.host_score]) > game_data[db_constant.local_total_point_threshold]

        self.logger.info('finished game judgement, total: {}'len(self.judgement))
        return

    def member_prediction_judge(self):
        pass

    def row_resulting(self, row):
        pass
