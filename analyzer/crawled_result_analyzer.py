from collections import defaultdict
from itertools import groupby

import numpy as np
import pandas as pd
import yaml

from config.constant import crawler as crawler_constant
from config.constant import database as db_constant
from config.constant import global_constant
from config.logger import get_logger
from database.constructor import DbConstructor


class CrawledResultAnalyzer(object):
    def __init__(self, to_db=False):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)

        self.db = DbConstructor.get_connection()
        self.to_db = to_db
        self.game_judgement = None
        self.prediction_judge_dict = dict.fromkeys((crawler_constant.all_member,
                                                    crawler_constant.all_prefer,
                                                    crawler_constant.more_than_sixty,
                                                    crawler_constant.top_100))
        self.prediction_judgement_summarize = defaultdict(dict)

    def start_analyzer(self):
        self.logger.info('start analyzer')
        game_data = self.get_game_data()
        self.judge(game_data)
        self.write_to_db(self.game_judgement, db_constant.game_judgement)

        for group in crawler_constant.prediction_group.keys():
            prediction_data = self.get_prediction_data(group)
            self.prediction_judge(prediction_data, group)
            self.write_to_db(self.prediction_judge_dict[group], '{}_{}'.format(db_constant.prediction_judgement, group))

        self.summarize_prediction_judgement()
        self.write_to_db(self.prediction_judgement_summarize, db_constant.prediction_judgement_summarize,
                         is_summarize=True)

        self.logger.info('analyzer done')
        return

    def get_game_data(self):
        self.logger.info('start get game data')
        return pd.read_sql('SELECT * FROM {}'.format(db_constant.game_data), con=self.db, index_col=db_constant.game_id)

    def get_prediction_data(self, group):
        self.logger.info('start get prediction data')
        return pd.read_sql('SELECT * FROM {}_{}'.format(db_constant.prediction_data, group), con=self.db,
                           index_col=db_constant.game_id)

    def judge(self, game_data):
        self.logger.info('start game result judge')

        self.game_judgement = pd.DataFrame(index=game_data.index)

        self.game_judgement[db_constant.host_win_original] = game_data[db_constant.guest_score] < game_data[
            db_constant.host_score]

        self.game_judgement[db_constant.host_win_point_spread_national] = game_data[db_constant.guest_score] < (
            game_data[db_constant.host_score] - game_data[db_constant.national_host_point_spread])

        self.game_judgement[db_constant.host_win_point_spread_local] = game_data[db_constant.guest_score] < (
            game_data[db_constant.host_score] - game_data[db_constant.local_host_point_spread])

        self.game_judgement[db_constant.over_total_point_national] = (game_data[db_constant.guest_score] +
                                                                      game_data[db_constant.host_score]) > game_data[
                                                                         db_constant.national_total_point_threshold]

        self.game_judgement[db_constant.over_total_point_local] = (game_data[db_constant.guest_score] + game_data[
            db_constant.host_score]) > game_data[db_constant.local_total_point_threshold]

        self.logger.info('finished game judgement, total: {}'.format(len(self.game_judgement)))
        return

    def prediction_judge(self, prediction_data, group):
        self.logger.info('start prediction judge, {}'.format(group))
        self.prediction_judge_dict[group] = pd.DataFrame(index=prediction_data.index)

        self.logger.debug('start judge local original')
        temp_target_prediction = prediction_data[db_constant.population_local_original_guest] < prediction_data[
            db_constant.population_local_original_host]
        self.prediction_judge_dict[group][db_constant.local_original_result] = temp_target_prediction == \
                                                                               self.game_judgement[
                                                                                   db_constant.host_win_original]
        self.prediction_judge_dict[group][db_constant.local_original_percentage] = np.where(
            self.game_judgement[db_constant.host_win_original],
            prediction_data[db_constant.percentage_local_original_host],
            prediction_data[db_constant.percentage_local_original_guest])
        self.prediction_judge_dict[group][db_constant.local_original_population] = np.where(
            self.game_judgement[db_constant.host_win_original],
            prediction_data[db_constant.population_local_original_host],
            prediction_data[db_constant.population_local_original_guest])

        self.logger.debug('start judge local total point')
        temp_target_prediction = prediction_data[db_constant.population_local_total_point_over] > prediction_data[
            db_constant.population_local_total_point_under]
        self.prediction_judge_dict[group][db_constant.local_total_point_result] = self.game_judgement[
                                                                                      db_constant.over_total_point_local] == temp_target_prediction
        self.prediction_judge_dict[group][db_constant.local_total_point_percentage] = np.where(
            self.game_judgement[db_constant.over_total_point_local],
            prediction_data[db_constant.percentage_local_total_point_over],
            prediction_data[db_constant.percentage_local_total_point_under])
        self.prediction_judge_dict[group][db_constant.local_total_point_population] = np.where(
            self.game_judgement[db_constant.over_total_point_local],
            prediction_data[db_constant.population_local_total_point_over],
            prediction_data[db_constant.population_local_total_point_under])

        self.logger.debug('start judge local point spread')
        temp_target_prediction = prediction_data[db_constant.population_local_point_spread_guest] < prediction_data[
            db_constant.population_local_point_spread_host]
        self.prediction_judge_dict[group][db_constant.local_point_spread_result] = self.game_judgement[
                                                                                       db_constant.host_win_point_spread_local] == temp_target_prediction
        self.prediction_judge_dict[group][db_constant.local_point_spread_percentage] = np.where(
            self.game_judgement[db_constant.host_win_point_spread_local],
            prediction_data[db_constant.percentage_local_point_spread_host],
            prediction_data[db_constant.percentage_local_point_spread_guest])
        self.prediction_judge_dict[group][db_constant.local_point_spread_population] = np.where(
            self.game_judgement[db_constant.host_win_point_spread_local],
            prediction_data[db_constant.population_local_point_spread_host],
            prediction_data[db_constant.population_local_point_spread_guest])

        self.logger.debug('start judge national total point')
        temp_target_prediction = prediction_data[db_constant.population_national_total_point_over] > prediction_data[
            db_constant.population_national_total_point_under]
        self.prediction_judge_dict[group][db_constant.national_total_point_result] = self.game_judgement[
                                                                                         db_constant.over_total_point_national] == temp_target_prediction
        self.prediction_judge_dict[group][db_constant.national_total_point_percentage] = np.where(
            self.game_judgement[db_constant.over_total_point_national],
            prediction_data[db_constant.percentage_national_total_point_over],
            prediction_data[db_constant.percentage_national_total_point_under])
        self.prediction_judge_dict[group][db_constant.national_total_point_population] = np.where(
            self.game_judgement[db_constant.over_total_point_national],
            prediction_data[db_constant.population_national_total_point_over],
            prediction_data[db_constant.population_national_total_point_under])

        self.logger.debug('start judge national point spread')
        temp_target_prediction = prediction_data[db_constant.population_national_point_spread_guest] < prediction_data[
            db_constant.population_national_point_spread_host]
        self.prediction_judge_dict[group][db_constant.national_point_spread_result] = self.game_judgement[
                                                                                          db_constant.host_win_point_spread_national] == temp_target_prediction
        self.prediction_judge_dict[group][db_constant.national_point_spread_percentage] = np.where(
            self.game_judgement[db_constant.host_win_point_spread_national],
            prediction_data[db_constant.percentage_national_point_spread_host],
            prediction_data[db_constant.percentage_national_point_spread_guest])
        self.prediction_judge_dict[group][db_constant.national_point_spread_population] = np.where(
            self.game_judgement[db_constant.host_win_point_spread_national],
            prediction_data[db_constant.population_national_point_spread_host],
            prediction_data[db_constant.population_national_point_spread_guest])

        self.logger.info('finished prediction judge, {}'.format(group))
        return

    def summarize_prediction_judgement(self):
        self.logger.info('start summarize prediction judgement')
        gambling_classes = (db_constant.national_point_spread_result[:-7],
                            db_constant.national_total_point_result[:-7],
                            db_constant.local_point_spread_result[:-7],
                            db_constant.local_total_point_result[:-7],
                            db_constant.local_original_result[:-7])
        for group in self.prediction_judge_dict.keys():
            table_name = '{}_{}'.format(db_constant.prediction_judgement, group)
            prediction_judgement = pd.read_sql('SELECT * FROM {}'.format(table_name),
                                               con=self.db, index_col=db_constant.game_id)
            for gambling_class in gambling_classes:
                self.sub_summarize(group, gambling_class, prediction_judgement)

        self.prediction_judgement_summarize = pd.DataFrame.from_dict(self.prediction_judgement_summarize).T
        self.prediction_judgement_summarize[db_constant.member_group] = self.prediction_judgement_summarize.index
        return

    def sub_summarize(self, group, gambling_class, prediction_judgement):
        # filter out gambling class and able to gambling games
        prediction_judgement = prediction_judgement.filter(regex=('{}'.format(gambling_class)))
        prediction_judgement = prediction_judgement[prediction_judgement['{}_population'.format(gambling_class)] != 0]

        win_ratio = sum(prediction_judgement['{}_result'.format(gambling_class)]) / len(prediction_judgement) if len(
            prediction_judgement) else 0
        max_continuous_lose = self._get_max_continuous_result(prediction_judgement, 0)

        self.prediction_judgement_summarize[group]['{}_{}'.format(gambling_class, db_constant.win_ratio)] = win_ratio
        self.prediction_judgement_summarize[group][
            '{}_{}'.format(gambling_class, db_constant.max_continuous_lose)] = max_continuous_lose
        self.prediction_judgement_summarize[group][
            '{}_{}'.format(gambling_class, db_constant.number_of_valid_game)] = len(prediction_judgement)

        return

    def _get_max_continuous_result(self, table, target):
        max_continuous = 0
        for row in table:
            for is_target, continuous in groupby(table[row], key=lambda x: x == target):
                if is_target:
                    max_continuous = max(max_continuous, len(list(continuous)))
        return max_continuous

    def write_to_db(self, df, table_name, is_summarize=False):
        if not self.to_db:
            self.logger.info('no need to write to db, skip write to db progress')
            return
        self.logger.info('start write game data to db: {}'.format(table_name))

        df.to_sql(con=self.engine,
                  name=table_name,
                  index_label='game_id' if not is_summarize else None,
                  index=not is_summarize,
                  if_exists='append',
                  schema=self.config[global_constant.DB][global_constant.schema])
        self.logger.info('finished write game data to db')
        self.db.connect()
        return
