import datetime

import pandas as pd
import pymysql
import yaml
from elasticsearch import Elasticsearch

from config.constant import converter
from config.constant import crawler
from config.constant import data_backup_scheduler
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

        for index, row in self.get_joined_table().iterrows():
            self.logger.debug('wipe game id: {}'.format(index))
            json_document = {}
            self.add_common_info(row, json_document, index)
            self.add_score(row, json_document)
            self.add_gamble_info(row, json_document)
            self.add_judgement_info(row, json_document)
            for group in crawler.prediction_group.keys():
                self.add_prediction_info(row, json_document, group)
                self.add_prediction_judgement_info(row, json_document, group)
            self.remove_nan_key(json_document)
            self.logger.debug('wiped document: {}'.format(json_document))
            self.es.index(index=row[db_constant.game_type].lower(), body=json_document)

    def add_common_info(self, row, json_document, index):
        self.logger.debug('add common info')
        json_document['@timestamp'] = datetime.datetime.strptime('{} {}'.format(row[db_constant.game_date],
                                                                                row[db_constant.play_time]),
                                                                 '{} {}'.format(self.config['crawler']['dateFormat'],
                                                                                '%I:%M'))
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
        json_document['prediction'][group] = {
            'national': {
                'total_point': {
                    'over': {
                        'percentage': row['{}__{}'.format(db_constant.percentage_national_total_point_over, group)],
                        'population': row['{}__{}'.format(db_constant.population_national_total_point_over, group)]},
                    'under': {
                        'percentage': row['{}__{}'.format(db_constant.percentage_national_total_point_over, group)],
                        'population': row['{}__{}'.format(db_constant.population_national_total_point_under, group)]}},
                'spread_point': {
                    db_constant.guest: {
                        'percentage': row['{}__{}'.format(db_constant.percentage_national_point_spread_guest, group)],
                        'population': row['{}__{}'.format(db_constant.population_national_point_spread_guest, group)]},
                    db_constant.host: {
                        'percentage': row['{}__{}'.format(db_constant.percentage_national_point_spread_host, group)],
                        'population': row['{}__{}'.format(db_constant.population_national_point_spread_host, group)]}}},
            'local': {
                'total_point': {
                    'over': {
                        'percentage': row['{}__{}'.format(db_constant.percentage_local_total_point_over, group)],
                        'population': row['{}__{}'.format(db_constant.population_local_total_point_over, group)]},
                    'under': {
                        'percentage': row['{}__{}'.format(db_constant.percentage_local_total_point_over, group)],
                        'population': row['{}__{}'.format(db_constant.population_local_total_point_under, group)]}},
                'spread_point': {
                    db_constant.guest: {
                        'percentage': row['{}__{}'.format(db_constant.percentage_local_point_spread_guest, group)],
                        'population': row['{}__{}'.format(db_constant.population_local_point_spread_guest, group)]},
                    db_constant.host: {
                        'percentage': row['{}__{}'.format(db_constant.percentage_local_point_spread_host, group)],
                        'population': row['{}__{}'.format(db_constant.population_local_point_spread_host, group)]}},
                'original': {
                    db_constant.guest: {
                        'percentage': row['{}__{}'.format(db_constant.percentage_local_original_guest, group)],
                        'population': row['{}__{}'.format(db_constant.population_local_original_guest, group)]},
                    db_constant.host: {
                        'percentage': row['{}__{}'.format(db_constant.percentage_local_original_host, group)],
                        'population': row['{}__{}'.format(db_constant.population_local_original_host, group)]}}}}

    def add_prediction_judgement_info(self, row, json_document, group):
        self.logger.debug('add prediction judgement info')
        json_document['judgement'] = json_document.get('judgement', {})
        json_document['judgement']['prediction'] = json_document['judgement'].get('prediction', {})
        json_document['judgement']['prediction'][group] = {
            'national': {
                'total_point': {
                    'matched_info': {
                        'is_major': bool(row['{}__{}'.format(db_constant.national_total_point_result, group)]),
                        'percentage': row['{}__{}'.format(db_constant.national_total_point_percentage, group)],
                        'population': row['{}__{}'.format(db_constant.national_total_point_population, group)]}},
                'spread_point': {
                    'matched_info': {
                        'is_major': bool(row['{}__{}'.format(db_constant.national_point_spread_result, group)]),
                        'percentage': row['{}__{}'.format(db_constant.national_point_spread_percentage, group)],
                        'population': row['{}__{}'.format(db_constant.national_point_spread_population, group)]}}},
            'local': {
                'total_point': {
                    'matched_info': {
                        'is_major': bool(row['{}__{}'.format(db_constant.local_total_point_result, group)]),
                        'percentage': row['{}__{}'.format(db_constant.local_total_point_percentage, group)],
                        'population': row['{}__{}'.format(db_constant.local_total_point_population, group)]}},
                'spread_point': {
                    'matched_info': {
                        'is_major': bool(row['{}__{}'.format(db_constant.local_point_spread_result, group)]),
                        'percentage': row['{}__{}'.format(db_constant.local_point_spread_percentage, group)],
                        'population': row['{}__{}'.format(db_constant.local_point_spread_population, group)]}},
                'original': {
                    'matched_info': {
                        'is_major': bool(row['{}__{}'.format(db_constant.local_original_result, group)]),
                        'percentage': row['{}__{}'.format(db_constant.local_original_percentage, group)],
                        'population': row['{}__{}'.format(db_constant.local_original_population, group)]}}}}

    def remove_nan_key(self, json_document):
        for k, v in list(json_document.items()):
            self.logger.debug('check: {}-{}'.format(k, v))
            if isinstance(v, dict):
                self.remove_nan_key(v)
            elif not pd.notnull(v):
                self.logger.debug('delete key-value: {}, {}'.format(k, v))
                json_document.pop(k, None)

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
