import yaml
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float

from config import constant
from config.logger import get_logger
from crawler import constant as crawler_constant
from database import constant


class DbConstructor(object):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml', 'r') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)

        # init db
        user = self.config[constant.DB][constant.user]
        password = self.config[constant.DB][constant.password]
        host = self.config[constant.DB][constant.host]
        self.engine = create_engine('mysql+pymysql://{}:{}@{}'.format(user, password, host))

    def create_schema(self, force=False):
        self.logger.info('start create schema, type force: {}'.format(force))
        if force:
            self.engine.execute(
                "DROP DATABASE IF EXISTS {}".format(self.config[constant.DB][constant.schema]))

        self.engine.execute(
            "CREATE DATABASE IF NOT EXISTS {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci".format(
                self.config[constant.DB][constant.schema]))
        return

    def create_tables(self):
        # self.engine.execute('USE {}'.format(self.config[string_constant.DB][string_constant.schema]))
        game_data = Table(constant.game_data, MetaData(),
                          Column(constant.game_id, String(12), primary_key=True),
                          Column(constant.play_time, String(10)),
                          Column(constant.am_pm, String(2)),
                          Column(constant.guest, String(10)),
                          Column(constant.host, String(10)),
                          Column(constant.guest_score, Integer),
                          Column(constant.host_score, Integer),
                          Column(constant.national_total_point_threshold, Float),
                          Column(constant.national_host_point_spread, Integer),
                          Column(constant.win_if_meet_spread_point, Integer),
                          Column(constant.response_ratio_if_hit_spread_point, Float),
                          Column(constant.local_host_point_spread, Float),
                          Column(constant.local_host_point_spread_response_ratio, Float),
                          Column(constant.local_total_point_threshold, Float),
                          Column(constant.local_total_point_threshold_response_ratio, Float),
                          Column(constant.local_origin_guest_response_ratio, Float),
                          Column(constant.local_origin_host_response_ratio, Float),
                          schema=self.config[constant.DB][constant.schema])

        # prediction table template for each prediction group
        def template(table_name): return Table('{}_{}'.format(constant.prediction_data, table_name), MetaData(),
                                               Column(constant.game_id, String(12), primary_key=True),
                                               Column(constant.percentage_national_point_spread_guest, Integer),
                                               Column(constant.population_national_point_spread_guest, Integer),
                                               Column(constant.percentage_national_total_point_guest, Integer),
                                               Column(constant.population_national_total_point_guest, Integer),
                                               Column(constant.percentage_local_point_spread_guest, Integer),
                                               Column(constant.population_local_point_spread_guest, Integer),
                                               Column(constant.percentage_local_total_point_guest, Integer),
                                               Column(constant.population_local_total_point_guest, Integer),
                                               Column(constant.percentage_local_original_guest, Integer),
                                               Column(constant.population_local_original_guest, Integer),
                                               Column(constant.percentage_national_point_spread_host, Integer),
                                               Column(constant.population_national_point_spread_host, Integer),
                                               Column(constant.percentage_national_total_point_host, Integer),
                                               Column(constant.population_national_total_point_host, Integer),
                                               Column(constant.percentage_local_point_spread_host, Integer),
                                               Column(constant.population_local_point_spread_host, Integer),
                                               Column(constant.percentage_local_total_point_host, Integer),
                                               Column(constant.population_local_total_point_host, Integer),
                                               Column(constant.percentage_local_original_host, Integer),
                                               Column(constant.population_local_original_host, Integer),
                                               schema=self.config[constant.DB][constant.schema])

        # create each table
        game_data.create(self.engine)
        template(crawler_constant.all_member).create(self.engine)
        template(crawler_constant.more_than_sixty).create(self.engine)
        template(crawler_constant.all_prefer).create(self.engine)
        template(crawler_constant.top_100).create(self.engine)
        return
