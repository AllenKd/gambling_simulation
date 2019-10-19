import pymysql
import yaml
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float

from config.constant import crawler as crawler_constant
from config.constant import database as db_constant
from config.constant import global_constant
from config.logger import get_logger


class DbConstructor(object):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml', 'r') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)

        # init db
        user = self.config[global_constant.DB][global_constant.user]
        password = self.config[global_constant.DB][global_constant.password]
        host = self.config[global_constant.DB][global_constant.host]
        port = self.config[global_constant.DB][global_constant.port]
        self.engine = create_engine('mysql+pymysql://{}:{}@{}:{}'.format(user, password, host, port))

    def create_schema(self, force=False):
        self.logger.info('start create schema, type force: {}'.format(force))
        if force:
            self.engine.execute(
                "DROP DATABASE IF EXISTS {}".format(self.config[global_constant.DB][global_constant.schema]))

        self.engine.execute(
            "CREATE DATABASE IF NOT EXISTS {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci".format(
                self.config[global_constant.DB][global_constant.schema]))
        return

    def create_tables(self):
        # self.engine.execute('USE {}'.format(self.config[string_constant.DB][string_constant.schema]))
        game_data = Table(db_constant.game_data, MetaData(),
                          Column(db_constant.row_id, Integer, primary_key=True, autoincrement='ignore_fk'),
                          Column(db_constant.game_date, Integer),
                          Column(db_constant.gamble_id, Integer),
                          Column(db_constant.game_type, String(16)),
                          Column(db_constant.play_time, String(10)),
                          Column(db_constant.am_pm, String(2)),
                          Column(db_constant.guest, String(10)),
                          Column(db_constant.host, String(10)),
                          Column(db_constant.guest_score, Integer),
                          Column(db_constant.host_score, Integer),
                          Column(db_constant.national_total_point_threshold, Float),
                          Column(db_constant.national_host_point_spread, Integer),
                          Column(db_constant.win_if_meet_spread_point, Integer),
                          Column(db_constant.response_ratio_if_hit_spread_point, Float),
                          Column(db_constant.local_host_point_spread, Float),
                          Column(db_constant.local_host_point_spread_response_ratio, Float),
                          Column(db_constant.local_total_point_threshold, Float),
                          Column(db_constant.local_total_point_threshold_response_ratio, Float),
                          Column(db_constant.local_origin_guest_response_ratio, Float),
                          Column(db_constant.local_origin_host_response_ratio, Float),
                          schema=self.config[global_constant.DB][global_constant.schema])

        game_judgement = Table(db_constant.game_judgement, MetaData(),
                               Column(db_constant.row_id, Integer, primary_key=True, autoincrement='ignore_fk'),
                               Column(db_constant.game_date, Integer),
                               Column(db_constant.gamble_id, Integer),
                               Column(db_constant.game_type, String(16)),
                               Column(db_constant.host_win_original, Integer),
                               Column(db_constant.host_win_point_spread_national, Integer),
                               Column(db_constant.host_win_point_spread_local, Integer),
                               Column(db_constant.over_total_point_national, Integer),
                               Column(db_constant.over_total_point_local, Integer),
                               schema=self.config[global_constant.DB][global_constant.schema])

        prediction_judgement_summarize = Table(db_constant.prediction_judgement_summarize, MetaData(),
                                               Column(db_constant.member_group, String(30)),
                                               Column(db_constant.national_point_spread_win_ratio, Float),
                                               Column(db_constant.national_point_spread_max_continuous_lose, Integer),
                                               Column(db_constant.national_point_spread_number_of_valid_game, Integer),
                                               Column(db_constant.national_total_point_win_ratio, Float),
                                               Column(db_constant.national_total_point_max_continuous_lose, Integer),
                                               Column(db_constant.national_total_point_number_of_valid_game, Integer),
                                               Column(db_constant.local_point_spread_win_ratio, Float),
                                               Column(db_constant.local_point_spread_max_continuous_lose, Integer),
                                               Column(db_constant.local_point_spread_number_of_valid_game, Integer),
                                               Column(db_constant.local_total_point_win_ratio, Float),
                                               Column(db_constant.local_total_point_max_continuous_lose, Integer),
                                               Column(db_constant.local_total_point_number_of_valid_game, Integer),
                                               Column(db_constant.local_original_win_ratio, Float),
                                               Column(db_constant.local_original_max_continuous_lose, Integer),
                                               Column(db_constant.local_original_number_of_valid_game, Integer),
                                               schema=self.config[global_constant.DB][global_constant.schema])

        # prediction judge table template for each prediction group
        def prediction_judgement_template(table_name): return Table(
            '{}_{}'.format(db_constant.prediction_judgement, table_name), MetaData(),
            Column(db_constant.row_id, Integer, primary_key=True, autoincrement='ignore_fk'),
            Column(db_constant.game_date, Integer),
            Column(db_constant.gamble_id, Integer),
            Column(db_constant.game_type, String(16)),
            Column(db_constant.national_point_spread_result, Integer),
            Column(db_constant.national_point_spread_percentage, Integer),
            Column(db_constant.national_point_spread_population, Integer),
            Column(db_constant.national_total_point_result, Integer),
            Column(db_constant.national_total_point_percentage, Integer),
            Column(db_constant.national_total_point_population, Integer),
            Column(db_constant.local_point_spread_result, Integer),
            Column(db_constant.local_point_spread_percentage, Integer),
            Column(db_constant.local_point_spread_population, Integer),
            Column(db_constant.local_total_point_result, Integer),
            Column(db_constant.local_total_point_percentage, Integer),
            Column(db_constant.local_total_point_population, Integer),
            Column(db_constant.local_original_result, Integer),
            Column(db_constant.local_original_percentage, Integer),
            Column(db_constant.local_original_population, Integer),
            schema=self.config[global_constant.DB][global_constant.schema])

        # prediction table template for each prediction group
        def template(table_name): return Table('{}_{}'.format(db_constant.prediction_data, table_name), MetaData(),
                                               Column(db_constant.row_id, Integer, primary_key=True,
                                                      autoincrement='ignore_fk'),
                                               Column(db_constant.game_date, Integer),
                                               Column(db_constant.gamble_id, Integer),
                                               Column(db_constant.game_type, String(16)),
                                               Column(db_constant.percentage_national_point_spread_guest, Integer),
                                               Column(db_constant.population_national_point_spread_guest, Integer),
                                               Column(db_constant.percentage_national_total_point_over, Integer),
                                               Column(db_constant.population_national_total_point_over, Integer),
                                               Column(db_constant.percentage_local_point_spread_guest, Integer),
                                               Column(db_constant.population_local_point_spread_guest, Integer),
                                               Column(db_constant.percentage_local_total_point_over, Integer),
                                               Column(db_constant.population_local_total_point_over, Integer),
                                               Column(db_constant.percentage_local_original_guest, Integer),
                                               Column(db_constant.population_local_original_guest, Integer),
                                               Column(db_constant.percentage_national_point_spread_host, Integer),
                                               Column(db_constant.population_national_point_spread_host, Integer),
                                               Column(db_constant.percentage_national_total_point_under, Integer),
                                               Column(db_constant.population_national_total_point_under, Integer),
                                               Column(db_constant.percentage_local_point_spread_host, Integer),
                                               Column(db_constant.population_local_point_spread_host, Integer),
                                               Column(db_constant.percentage_local_total_point_under, Integer),
                                               Column(db_constant.population_local_total_point_under, Integer),
                                               Column(db_constant.percentage_local_original_host, Integer),
                                               Column(db_constant.population_local_original_host, Integer),
                                               schema=self.config[global_constant.DB][global_constant.schema])

        # create each table
        self.create_if_not_exist(game_data)
        self.create_if_not_exist(game_data)
        self.create_if_not_exist(game_judgement)
        self.create_if_not_exist(prediction_judgement_summarize)
        self.create_if_not_exist(template(crawler_constant.all_member))
        self.create_if_not_exist(template(crawler_constant.more_than_sixty))
        self.create_if_not_exist(template(crawler_constant.all_prefer))
        self.create_if_not_exist(template(crawler_constant.top_100))

        self.create_if_not_exist(prediction_judgement_template(crawler_constant.all_member))
        self.create_if_not_exist(prediction_judgement_template(crawler_constant.more_than_sixty))
        self.create_if_not_exist(prediction_judgement_template(crawler_constant.all_prefer))
        self.create_if_not_exist(prediction_judgement_template(crawler_constant.top_100))

        return

    def create_if_not_exist(self, table):
        if table.exists(bind=self.engine):
            self.logger.info('table {} already exist, skip creation'.format(table.name))
            return
        self.logger.info('create table: {}'.format(table.name))
        table.create(self.engine)
