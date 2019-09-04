import datetime

import pandas as pd
import pymysql
import yaml
from elasticsearch import Elasticsearch

from config.constant import data_backup_scheduler
from config.constant import converter
from config.constant import database as db_constant
from config.constant import global_constant
from config.logger import get_logger


class NoSqlConverter(object):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)

        # create db connection
        user = self.config[global_constant.DB][global_constant.user]
        password = self.config[global_constant.DB][global_constant.password]
        host = self.config[global_constant.DB][global_constant.host]
        port = self.config[global_constant.DB][global_constant.port]
        self.db = pymysql.connect(host=host, user=user, passwd=password, port=port,
                                  db=self.config[global_constant.DB][global_constant.schema], charset='utf8')

        self.es = Elasticsearch([{'host': host, 'port': 9200}])

    def start_convert(self):
        self.logger.info('start converter')
        json_document = {}
        a = self.get_joined_table()
        for table_name, data in self.iter_table_as_df():
            for index, row in data.iterrows():
                self.add_common_info(row, json_document, index)
                if table_name == db_constant.game_data:
                    self.add_score(row, json_document)
                    self.add_gamble_info(row, json_document)

                    # self.es.index(index=table_name, body=json_document)

                if table_name == db_constant.game_judgement:
                    self.add_judgement_info(row, json_document)

                    # self.es.index(index=table_name, body=json_document)

                if table_name.startswith(db_constant.prediction_data):
                    group = table_name[16:]
                    self.add_prediction_info(row, json_document, group)

                if table_name.startswith(db_constant.prediction_judgement):
                    group = table_name[21:]
                    self.add_prediction_judgement_info(row, json_document, group)

    def add_common_info(self, row, json_document, index):
        self.logger.debug('add common info')
        json_document['timestamp'] = str(
            datetime.datetime.strptime('{} {}'.format(row[db_constant.game_date], row[db_constant.play_time]),
                                       '{} {}'.format(self.config['crawler']['dateFormat'], '%I:%M')))
        json_document['game_id'] = index
        json_document[db_constant.gamble_id] = row[db_constant.gamble_id]
        json_document[db_constant.game_type] = row[db_constant.game_type]
        return json_document

    def add_score(self, row, json_document):
        self.logger.debug('add score')
        json_document[db_constant.guest] = {'name': row[db_constant.guest],
                                            'score': row[db_constant.guest_score]}

        json_document[db_constant.host] = {'name': row[db_constant.host],
                                           'score': row[db_constant.host_score]}
        return json_document

    def add_gamble_info(self, row, json_document):
        self.logger.debug('add gamble info')
        json_document['gamble_info'] = {}
        json_document['gamble_info']['national'] = {
            'total_point': {'threshold': row[db_constant.national_total_point_threshold]},
            'spread_point': {db_constant.host: row[db_constant.national_host_point_spread],
                             'response': {'on_hit': row[
                                 db_constant.response_ratio_if_hit_spread_point]}}}
        json_document['gamble_info']['local'] = {
            'total_point': {'threshold': row[db_constant.local_total_point_threshold],
                            'response': row[
                                db_constant.local_total_point_threshold_response_ratio]},
            'spread_point': {db_constant.host: row[db_constant.local_host_point_spread],
                             'response': {db_constant.host: row[
                                 db_constant.local_host_point_spread_response_ratio]}},
            'original': {'response': {
                db_constant.guest: row[db_constant.local_origin_guest_response_ratio],
                db_constant.host: row[db_constant.local_origin_host_response_ratio]}}}
        return json_document

    def add_judgement_info(self, row, json_document):
        self.logger.debug('add judgement info')
        json_document['judgement'] = json_document.get('judgement', {})
        json_document['judgement']['game'] = json_document['judgement'].get('game', {})
        json_document['judgement']['game']['national'] = {
            'over_threshold': bool(row[db_constant.over_total_point_national]),
            'spread_point': 'host' if row[
                db_constant.host_win_point_spread_national] else 'guest'}
        json_document['judgement']['game']['local'] = {'over_threshold': bool(row[db_constant.over_total_point_local]),
                                                       'spread_point': 'host' if row[
                                                           db_constant.host_win_point_spread_local] else 'guest',
                                                       'original': 'host' if row[
                                                           db_constant.host_win_original] else 'guest'}

    def add_prediction_info(self, row, json_document, group):
        self.logger.debug('add prediction info')
        json_document['prediction'] = json_document.get('prediction', {})
        json_document['prediction']['group'] = {
            'group': group,
            'national': {'total_point': {'over': {'percentage': row[db_constant.percentage_national_total_point_over],
                                                  'population': row[db_constant.population_national_total_point_over]},
                                         'under': {'percentage': row[db_constant.percentage_national_total_point_over],
                                                   'population': row[
                                                       db_constant.population_national_total_point_under]}},
                         'spread_point': {
                             db_constant.guest: {'percentage': row[db_constant.percentage_national_point_spread_guest],
                                                 'population': row[db_constant.population_national_point_spread_guest]},
                             db_constant.host: {'percentage': row[db_constant.percentage_national_point_spread_host],
                                                'population': row[db_constant.population_national_point_spread_host]}}},
            'local': {'total_point': {'over': {'percentage': row[db_constant.percentage_local_total_point_over],
                                               'population': row[db_constant.population_local_total_point_over]},
                                      'under': {'percentage': row[db_constant.percentage_local_total_point_over],
                                                'population': row[db_constant.population_local_total_point_under]}},
                      'spread_point': {
                          db_constant.guest: {'percentage': row[db_constant.percentage_local_point_spread_guest],
                                              'population': row[db_constant.population_local_point_spread_guest]},
                          db_constant.host: {'percentage': row[db_constant.percentage_local_point_spread_host],
                                             'population': row[db_constant.population_local_point_spread_host]}},
                      'original': {db_constant.guest: {'percentage': row[db_constant.percentage_local_original_guest],
                                                       'population': row[db_constant.population_local_original_guest]},
                                   db_constant.host: {'percentage': row[db_constant.percentage_local_original_host],
                                                      'population': row[db_constant.population_local_original_host]}}}}

    def add_prediction_judgement_info(self, row, json_document, group):
        self.logger.debug('add prediction judgement info')
        json_document['judgement'] = {}
        json_document['judgement']['prediction'] = {}
        json_document['judgement']['prediction'] = {
            'group': group,
            'national': {
                'total_point': {'matched_info': {'is_major': bool(row[db_constant.national_total_point_result]),
                                                 'percentage': row[db_constant.national_total_point_percentage],
                                                 'population': row[db_constant.national_total_point_population]}},
                'spread_point': {'matched_info': {'is_major': bool(row[db_constant.national_point_spread_result]),
                                                  'percentage': row[db_constant.national_point_spread_percentage],
                                                  'population': row[db_constant.national_point_spread_population]}}},
            'local': {
                'total_point': {'matched_info': {'is_major': bool(row[db_constant.local_total_point_result]),
                                                 'percentage': row[db_constant.local_total_point_percentage],
                                                 'population': row[db_constant.local_total_point_population]}},
                'spread_point': {'matched_info': {'is_major': bool(row[db_constant.local_point_spread_result]),
                                                  'percentage': row[db_constant.local_point_spread_percentage],
                                                  'population': row[db_constant.local_point_spread_population]}},
                'original': {'matched_info': {'is_major': bool(row[db_constant.local_original_result]),
                                              'percentage': row[db_constant.local_original_percentage],
                                              'population': row[db_constant.local_original_population]}}}}

    def iter_table_as_df(self):
        self.logger.info('start iterate db')
        # cursor = self.db.cursor()
        # cursor.execute('SHOW TABLES')
        for table_name in data_backup_scheduler.table_list:
            self.logger.debug('get table: {}'.format(table_name))
            yield table_name, pd.read_sql('SELECT * FROM {} LIMIT 10'.format(table_name), con=self.db,
                                          index_col=db_constant.row_id)

    def get_joined_table(self):
        self.logger.info('start get joined table')
        sql_select = 'SELECT {} FROM {} '.format(', '.join(converter.joined_columns), db_constant.game_data)
        sql_join = ' '.join(['LEFT JOIN {} ON {}.id={}.id'.format(table_name, table_name, 'game_data')
                             for table_name in data_backup_scheduler.table_list if table_name != db_constant.game_data])
        sql = sql_select + sql_join
        return pd.read_sql(sql, con=self.db, index_col=db_constant.row_id)

