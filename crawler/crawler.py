import datetime
import re
from collections import defaultdict

import pandas as pd
import requests
import yaml
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

from config.constant import crawler as crawler_constant
from config.constant import database as db_constant
from config.constant import global_constant
from config.logger import get_logger


class Crawler(object):
    def __init__(self, start_date, end_date):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)
        self.data = None
        self.game_info = defaultdict(list)
        self.prediction_info_all_member = defaultdict(list)
        self.prediction_info_more_than_sixty = defaultdict(list)
        self.prediction_info_all_prefer = defaultdict(list)
        self.prediction_info_top_100 = defaultdict(list)

        self.prediction = {crawler_constant.all_member: self.prediction_info_all_member,
                           crawler_constant.more_than_sixty: self.prediction_info_more_than_sixty,
                           crawler_constant.all_prefer: self.prediction_info_all_prefer,
                           crawler_constant.top_100: self.prediction_info_top_100}

        # setup datetime object and count total days
        self.start_date = datetime.datetime.strptime(start_date, self.config['crawler']['dateFormat'])
        self.end_date = datetime.datetime.strptime(end_date, self.config['crawler']['dateFormat'])
        self.total_day = self.end_date - self.start_date

        # init db
        user = self.config[global_constant.DB][global_constant.user]
        password = self.config[global_constant.DB][global_constant.password]
        host = self.config[global_constant.DB][global_constant.host]
        self.engine = create_engine('mysql+pymysql://{}:{}@{}'.format(user, password, host))

    def start_crawler(self):
        total_crawled_game = 0
        # crawl for each date
        for date in pd.date_range(start=self.start_date, end=self.end_date):
            date = datetime.datetime.strftime(date, self.config['crawler']['dateFormat'])
            # crawl for each prediction group
            for prediction_group in crawler_constant.prediction_group.keys():
                res = requests.get(self.get_url(date, crawler_constant.prediction_group[prediction_group]))
                soup = BeautifulSoup(res.text, 'html.parser')
                if prediction_group == crawler_constant.all_member:
                    # get game info for once
                    self.get_game_data(date, soup)
                    self.write_to_db(pd.DataFrame.from_dict(self.game_info), db_constant.game_data)
                    # clean cache after write to db
                    total_crawled_game += len(self.game_info[db_constant.game_id])
                    self.game_info = defaultdict(list)

                # get prediction info for each prediction group
                self.get_prediction_data(date, soup, prediction_group)
                self.write_to_db(pd.DataFrame.from_dict(self.prediction[prediction_group]),
                                 '{}_{}'.format(db_constant.prediction_data, prediction_group))
                # clean cache after write to db
                self.prediction[prediction_group] = defaultdict(list)

        self.logger.info(
            'crawler task done, total crawled games: {}, days: {}'.format(total_crawled_game, self.total_day.days))
        return

    def get_game_data(self, date, soup):
        self.logger.info('start crawl and parse game data: {}'.format(date))
        custom_row = True
        for row_content in soup.find('tbody').findAll('tr', {'class': 'game-set'}):
            if custom_row:
                assert self.check_data_consistent(self.game_info)
                self.append_game_id(row_content, date)
                self.append_game_time(row_content)
                self.append_team_name(row_content)
                self.append_score(row_content)
                self.append_total_point_info(row_content)
            self.append_point_spread_info(row_content, custom_row)
            self.append_response_ratio_info(row_content, custom_row)
            custom_row = not custom_row
        self.logger.info('finished crawl and parse game data: {}'.format(date))
        return

    def get_prediction_data(self, date, soup, group):
        self.logger.info('start crawl and parse prediction data: {}'.format(date))
        guest_row = True
        for row_content in soup.find('tbody').findAll('tr', {'class': 'game-set'}):
            if guest_row:
                assert self.check_data_consistent(self.prediction[group])
                self.append_game_id(row_content, date, group)
            self.append_prediction_national_point_spread(row_content, guest_row, group)
            self.append_prediction_national_total_point(row_content, guest_row, group)
            self.append_prediction_local_point_spread(row_content, guest_row, group)
            self.append_prediction_local_total_point(row_content, guest_row, group)
            self.append_prediction_local_original(row_content, guest_row, group)
            guest_row = not guest_row
        self.logger.info('finished crawl and parse prediction data: {}'.format(date))
        return

    def append_prediction_national_point_spread(self, row_content, guest_row, group):
        date = row_content.find('td', {'class': 'td-universal-bet01'}).find_next('td').text.strip()
        date = re.findall(r'\d+', date)
        percentage, population = date if len(date) == 2 else (0, 0)
        if guest_row:
            self.prediction[group][db_constant.percentage_national_point_spread_guest].append(percentage)
            self.prediction[group][db_constant.population_national_point_spread_guest].append(population)
        else:
            self.prediction[group][db_constant.percentage_national_point_spread_host].append(percentage)
            self.prediction[group][db_constant.population_national_point_spread_host].append(population)
        return

    def append_prediction_national_total_point(self, row_content, guest_row, group):
        date = row_content.find('td', {'class': 'td-universal-bet02'}).find_next('td').text.strip()
        date = re.findall(r'\d+', date)
        percentage, population = date if len(date) == 2 else (0, 0)
        if guest_row:
            self.prediction[group][db_constant.percentage_national_total_point_over].append(percentage)
            self.prediction[group][db_constant.population_national_total_point_over].append(population)
        else:
            self.prediction[group][db_constant.percentage_national_total_point_under].append(percentage)
            self.prediction[group][db_constant.population_national_total_point_under].append(population)
        return

    def append_prediction_local_point_spread(self, row_content, guest_row, group):
        date = row_content.find('td', {'class': 'td-bank-bet01'}).find_next('td').text.strip()
        date = re.findall(r'\d+', date)
        percentage, population = date if len(date) == 2 else (0, 0)
        if guest_row:
            self.prediction[group][db_constant.percentage_local_point_spread_guest].append(percentage)
            self.prediction[group][db_constant.population_local_point_spread_guest].append(population)
        else:
            self.prediction[group][db_constant.percentage_local_point_spread_host].append(percentage)
            self.prediction[group][db_constant.population_local_point_spread_host].append(population)
        return

    def append_prediction_local_total_point(self, row_content, guest_row, group):
        date = row_content.find('td', {'class': 'td-bank-bet02'}).find_next('td').text.strip()
        date = re.findall(r'\d+', date)
        percentage, population = date if len(date) == 2 else (0, 0)
        if guest_row:
            self.prediction[group][db_constant.percentage_local_total_point_over].append(percentage)
            self.prediction[group][db_constant.population_local_total_point_over].append(population)
        else:
            self.prediction[group][db_constant.percentage_local_total_point_under].append(percentage)
            self.prediction[group][db_constant.population_local_total_point_under].append(population)
        return

    def append_prediction_local_original(self, row_content, guest_row, group):
        date = row_content.find('td', {'class': 'td-bank-bet03'}).find_next('td').text.strip()
        date = re.findall(r'\d+', date)
        percentage, population = date if len(date) == 2 else (0, 0)
        if guest_row:
            self.prediction[group][db_constant.percentage_local_original_guest].append(percentage)
            self.prediction[group][db_constant.population_local_original_guest].append(population)
        else:
            self.prediction[group][db_constant.percentage_local_original_host].append(percentage)
            self.prediction[group][db_constant.population_local_original_host].append(population)
        return

    def append_game_id(self, row_content, date, group=None):
        game_id = date + row_content.find('td', 'td-gameinfo').find('h3').text

        if group:
            self.logger.debug(
                'current column size of {}: {}'.format(db_constant.game_id,
                                                       len(self.prediction[group][db_constant.game_id])))
            self.prediction[group][db_constant.game_id].append(game_id)
        else:
            self.logger.debug(
                'current column size of {}: {}'.format(db_constant.game_id, len(self.game_info[db_constant.game_id])))
            self.game_info[db_constant.game_id].append(game_id)

        self.logger.info('append game id: {}'.format(game_id))
        return

    def append_game_time(self, row_content):
        self.logger.info(
            'current column size of {}: {}'.format(db_constant.play_time, len(self.game_info[db_constant.play_time])))
        game_time = row_content.find('td', 'td-gameinfo').find('h4').text
        apm, time = game_time.split()
        self.logger.info('append play time: {}'.format(game_time))
        self.game_info[db_constant.play_time].append(time)
        self.game_info[db_constant.am_pm].append(apm)
        return

    def append_score(self, row_content):
        self.logger.info(
            'current column size of {}: {}'.format(db_constant.guest_score,
                                                   len(self.game_info[db_constant.guest_score])))
        self.logger.info(
            'current column size of {}: {}'.format(db_constant.host_score, len(self.game_info[db_constant.host_score])))
        guest = int(row_content.find('td', {'class': 'td-teaminfo'}).find_all('li')[0].text.strip())
        host = int(row_content.find('td', {'class': 'td-teaminfo'}).find_all('li')[-1].text.strip())
        self.logger.debug('append guest: {}, host: {}'.format(guest, host))
        self.game_info[db_constant.guest_score].append(guest)
        self.game_info[db_constant.host_score].append(host)
        return

    def append_team_name(self, row_content):
        self.logger.info(
            'current column size of {}: {}'.format(db_constant.guest_id, len(self.game_info[db_constant.guest])))
        self.logger.info(
            'current column size of {}: {}'.format(db_constant.host_id, len(self.game_info[db_constant.host])))

        guest = row_content.find('td', {'class': 'td-teaminfo'}).find_all('tr')[0].find('a').text.strip()
        host = row_content.find('td', {'class': 'td-teaminfo'}).find_all('tr')[-1].find('a').text.strip()

        guest_abbreviate = crawler_constant.team_name_mapping[
            guest] if guest in crawler_constant.team_name_mapping.keys() else guest
        host_abbreviate = crawler_constant.team_name_mapping[
            host] if host in crawler_constant.team_name_mapping.keys() else host

        self.logger.debug('append guest: {}, host: {}'.format(guest, host))
        self.game_info[db_constant.guest].append(guest_abbreviate)
        self.game_info[db_constant.host].append(host_abbreviate)
        return

    def append_point_spread_info(self, row_content, custom_row):
        spread_info = row_content.find('td', {'class': 'td-universal-bet01'}).text.strip()
        if len(spread_info) != 1:
            # get national point spread info
            self.logger.debug('the row contains national spread point info')
            national_spread_from = crawler_constant.chinese_mapping[spread_info[0]]
            national_spread_point, hit_percentage = re.findall(r'\d+', spread_info)
            hit_result = crawler_constant.chinese_mapping[re.findall(r'[輸贏]', spread_info)[0]]
            hit_percentage = int(hit_percentage) + 100 if hit_result else int(hit_percentage)
            national_spread_point = -int(national_spread_point) if national_spread_from == db_constant.guest else int(
                national_spread_point)
            self.game_info[db_constant.national_host_point_spread].append(national_spread_point)
            self.game_info[db_constant.win_if_meet_spread_point].append(hit_result)
            self.game_info[db_constant.response_ratio_if_hit_spread_point].append(hit_percentage / 100)

        if custom_row:
            # get local point spread info and response ratio
            local_host_spread_point = row_content.find('td', {'class': 'td-bank-bet01'}).text.strip()
            # filter out float
            data = re.findall(r'[+-]?\d+\.\d+', local_host_spread_point)
            local_host_spread_point, spread_point_response_ratio = data if len(data) == 2 else (0, 0)
            self.game_info[db_constant.local_host_point_spread].append(float(local_host_spread_point))
            self.game_info[db_constant.local_host_point_spread_response_ratio].append(
                float(spread_point_response_ratio))

            # get local total point info and response ratio
            local_total_point = row_content.find('td', {'class': 'td-bank-bet02'}).text.strip()
            # filter out float
            data = re.findall(r'\d+\.\d+', local_total_point)
            local_total_point, total_point_response = data if len(data) == 2 else (0, 0)
            self.game_info[db_constant.local_total_point_threshold].append(float(local_total_point))
            self.game_info[db_constant.local_total_point_threshold_response_ratio].append(float(total_point_response))

        return

    def append_total_point_info(self, row_content):
        # get national total point info
        national_total_point = row_content.find('td', {'class': 'td-universal-bet02'}).text.strip()
        threshold = re.findall(r'\d+[\.\d+]?', national_total_point)
        national_total_point = threshold[0] if threshold else 0
        self.game_info[db_constant.national_total_point_threshold].append(float(national_total_point))
        pass

    def append_response_ratio_info(self, row_content, guest_row):
        self.logger.info('append response ratio info')
        if guest_row:
            # get guest response ratio of no point spread at local
            local_origin_guest_response_ratio = row_content.find('td', {'class': 'td-bank-bet03'}).text.strip()
            ratio = re.findall(r'\d+\.\d+', local_origin_guest_response_ratio)
            local_origin_guest_response_ratio = ratio[0] if ratio else 0
            self.game_info[db_constant.local_origin_guest_response_ratio].append(
                float(local_origin_guest_response_ratio))
        else:
            # get host response ratio of no point spread at local
            local_origin_host_response_ratio = row_content.find('td', {'class': 'td-bank-bet03'}).text.strip()
            ratio = re.findall(r'\d+\.\d+', local_origin_host_response_ratio)
            local_origin_host_response_ratio = ratio[0] if ratio else 0
            self.game_info[db_constant.local_origin_host_response_ratio].append(float(local_origin_host_response_ratio))

    def write_to_db(self, df, table_name):
        self.logger.info('start write game data to db: {}'.format(table_name))
        df.to_sql(con=self.engine,
                  name=table_name,
                  index_label='game_id',
                  index=False,
                  if_exists='append',
                  schema=self.config[global_constant.DB][global_constant.schema])
        self.logger.info('finished write game data to db')
        return

    def check_data_consistent(self, table):
        length_list = [len(i) for i in table.values()]
        return length_list.count(length_list[0]) == len(length_list) if length_list else True

    def get_url(self, date, member_type=1):
        return self.config['crawler']['urlPattern'].format(date, member_type)
